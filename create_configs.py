#! /usr/bin/env python3

import yaml
import argparse
import pathlib
import subprocess
import shlex
import copy
import datetime
import shutil

from crab_configuration.crab_template import config


# TODO:
# Introduce an option --exclude-sites-by-pattern,
# which leads to a more sophisticated choice of site where to run
# Based on dataset placement, to be checked with dasgoclient command


def parse_args():
    parser = argparse.ArgumentParser(
        description="Script to prepare a CMSSW production with crab",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Main options

    ## Necessary arguments
    parser.add_argument("--work-directory", required=True, help="Path to the main work directory")
    parser.add_argument("--datasets", required=True, help="Path to the dataset configuration .yaml file")

    ## Optional arguments
    # Either provide a config listing the locations of the ready cmsRun python configs, or provide the cmsDriver configs (`cmsdriver` and `conditions` configs)

    # cmsdriver configuration group
    cmssw_config = parser.add_argument_group("CMSSW config", "Configuration related to already present cmsRun configs. Either this or the \"cmsDriver\" option has to be provided.")

    ## config with cmssw python config files:
    cmssw_config.add_argument("--cmssw-configs", help="Path to a .yaml file listing the locations of the ready cmsRun python config files. The keys of this config have to be the same as the keys in the conditions configuration file, e.g. data and mc. Can be used as an alternative to providing cmsDriver configuration files. If provided, the cmsRun config files listed in this config will be copied to the cmsdriver directory and no cmsDriver command will be run.")
    
    cmsdriver = parser.add_argument_group("cmsDriver", "Configuration related to cmsDriver settings to generate a cmsRun config. Either this or the \"CMSSW config\" option has to be provided.")
    
    ## Necessary arguments for cmsDriver configuration:
    cmsdriver.add_argument("--conditions", help="Path to the conditions configuration .yaml file, which contains the globaltag and era information for the cmsDriver command. The keys of this config have to be the same as the keys in the cmsDriver configuration file, e.g. data and mc.")
    cmsdriver.add_argument("--cmsdriver", help="Path to the cmsDriver configuration .yaml file, which contains general configuration for the cmsDriver command, e.g. type, filein, fileout, step, eventcontent, datatier, python_filename. The keys of this config have to be the same as the keys in the conditions configuration file, e.g. data and mc.")
    cmsdriver.add_argument("--nThreads", type=int, default=1, help="Number of threads to be used for the cmsRun config")
    cmsdriver.add_argument("--nStreams", type=int, default=0, help="Number of streams to be used for the cmsRun config. If set to 0, nThreads will be taken by cmsRun.")

    # Crab configuration group
    crab = parser.add_argument_group(
        "crab3", "Configuration related to crab3 settings to submit a crab task")

    ## Optional arguments
    crab.add_argument("--numCores", type=int, default=1, help="Number of Cores used by crab for the job")
    crab.add_argument("--maxMemoryMBperCore", type=int, default=2000, help="Maximum memory in MB to be used by the crab job per core")
    crab.add_argument("--maxJobRuntimeMin", type=int, default=720, help="Maximum runtime expected for the job im minutes")
    crab.add_argument("--publication", action="store_true", help="Flag to decide, whether to publish crab output dataset")
    crab.add_argument("--splitting", choices=["Automatic", "FileBased", "LumiBased", "EventAwareLumiBased"], default="Automatic", help="Choice of splitting of the task into jobs.")
    crab.add_argument("--unitsPerJob", type=int, default=720, help="Rough number of files (FileBased), luminosity sections (LumiBased), or events (EventAwareLumiBased) to have per job, depending on the corresponding splitting. In case of Automatic splitting: target runtime in minutes with a minimum of 180.")
    crab.add_argument("--siteWhitelist", nargs="*", help="List of sites to exclusively run your jobs on.")
    crab.add_argument("--siteBlacklist", nargs="*", help="List of sites to avoid running your jobs there.")

    return parser.parse_args()


def initialize(args):
    args_dict = vars(args)
    # Check if inputDBS is provided in the dataset configuration file, if not, add it with the default value "global"
    datasets = yaml.safe_load(open(args_dict["datasets"], "r"))
    args_dict["inputDBS"] = datasets.pop("inputDBS", "global")
    args_dict["datasets"] = datasets
    # check if cmssw_configs is provided, if so, add it to the args_dict, if not, check if cmsdriver and conditions are provided, if so, add them to the args_dict, if not, raise an error
    if args_dict.get("cmssw_configs", None) is not None:
        args_dict["cmssw_configs"] = yaml.safe_load(open(args_dict["cmssw_configs"], "r"))
    elif args_dict.get("conditions", None) is not None and args_dict.get("cmsdriver", None) is not None:
        args_dict["conditions"] = yaml.safe_load(open(args_dict["conditions"], "r"))
        args_dict["cmsdriver"] = yaml.safe_load(open(args_dict["cmsdriver"], "r"))
    else:
        raise ValueError("Either 'cmssw_configs' or both 'conditions' and 'cmsdriver' must be provided.")

    args_dict["crab"] = config
    args_dict["timestamp"] = str(int(datetime.datetime.now().timestamp()))
    return args_dict


def prepare(args):
    # Ensure, that work directory exists
    work_directory = pathlib.Path(args["work_directory"])
    work_directory.mkdir(mode=0o755, parents=True, exist_ok=True)

    # Prepare cmsDriver commands and create cmsRun configs
    cmssw_config_dir = work_directory / "cmssw_configs"
    cmssw_config_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    # If cmssw_configs is provided, copy the cmsRun configs to the cmssw_config_dir and add the path to the cmsRun config
    if args.get("cmssw_configs", None):
        for k, dt_period in args["cmssw_configs"].items():
            for dt, config_file in dt_period.items():
                # copy cmssw config to cmsdriver directory
                cmsrun = cmssw_config_dir / f"{k}_{dt}_cmssw_config.py"
                shutil.copy(config_file, cmsrun)
                args["cmssw_configs"][k][dt] = cmsrun
    else:
        # Check that the keys in the cmsdriver and conditions config are the same, e.g. data and mc
        cmsdriver_keys = set(args["cmsdriver"].keys())
        conditions_keys = set(args["conditions"].keys())
        assert cmsdriver_keys == conditions_keys, f"cmsdriver keys {cmsdriver_keys} must match conditions keys {conditions_keys}"

        for k, cmsdriverspecs in args["cmsdriver"].items():
            for dt_period, configuration in args["conditions"][k].items():
                cmsrundir = cmssw_config_dir / str(dt_period)
                cmsrundir.mkdir(mode=0o755, parents=True, exist_ok=True)
                cmsrun = cmsrundir / cmsdriverspecs["python_filename"]
                args["conditions"][k][dt_period]["cmsrun"] = cmsrun
                command = f'cmsDriver.py {cmsdriverspecs["type"]} --{k if k in ["data", "mc"] else "data"} --filein file:{cmsdriverspecs["filein"]} --fileout {cmsdriverspecs["fileout"]} --step {cmsdriverspecs["step"]} --eventcontent {cmsdriverspecs["eventcontent"]} --datatier {cmsdriverspecs["datatier"]} --python_filename {str(cmsrun)} --conditions {configuration["globaltag"]} --era {configuration["era"]} --no_exec --nThreads {args["nThreads"]} --nStreams {args["nStreams"]}'
                print(f"Running: {command}")
                # TODO: introduce a checksum check to be sure, that the new round creates the same config, if one exists.
                result = subprocess.run(
                    shlex.split(command), capture_output=True, text=True
                )
                print(f"\tReturn code: {result.returncode}")

    # Construct general crab config based on provided crab3 settings
    crabworkarea = work_directory / "crab"
    crabworkarea.mkdir(mode=0o755, parents=True, exist_ok=True)
    crabconfigarea = work_directory / "crabconfigs"
    crabconfigarea.mkdir(mode=0o755, parents=True, exist_ok=True)
    args["crab"].General.workArea = str(crabworkarea)
    args["crab"].JobType.numCores = args["numCores"]
    args["crab"].JobType.maxMemoryMB = args["maxMemoryMBperCore"] * args["numCores"]
    args["crab"].JobType.maxJobRuntimeMin = args["maxJobRuntimeMin"]
    args["crab"].Data.publication = args["publication"]
    args["crab"].Data.splitting = args["splitting"]
    args["crab"].Data.unitsPerJob = args["unitsPerJob"]
    args["crab"].Site.whitelist = args["siteWhitelist"]
    args["crab"].Site.blacklist = args["siteBlacklist"]
    args["crab"].Data.inputDBS = args["inputDBS"]
    print("\nGeneral crab configuration:")
    print(args["crab"])

    args["crabconfigs"] = {}
    # Loop through the datasets and create dataset-specific crab configuration files
    for k, dt_period_config in args["datasets"].items():  # k is key from {data, mc}
        args["crabconfigs"][k] = {}
        for dt_period, dataset_type_config in dt_period_config.items():
            args["crabconfigs"][k][dt_period] = {}
            for dataset_type, datasets in dataset_type_config.items():
                args["crabconfigs"][k][dt_period][dataset_type] = {}
                for dkey, dname in datasets.items():
                    dataset_crab = copy.deepcopy((args["crab"]))
                    dataset_crab.General.requestName = "_".join(
                        [k, dt_period, dataset_type, dkey]
                    )
                    if args.get("cmssw_configs", None):
                        dataset_crab.JobType.psetName = str(args["cmssw_configs"][k][dt_period])
                    else:
                        dataset_crab.JobType.psetName = str(args["conditions"][k][dt_period]["cmsrun"])
                    dataset_crab.Data.inputDataset = dname
                    dataset_crab.Data.outputDatasetTag = (
                        dataset_crab.General.requestName + "_" + args["timestamp"]
                    )
                    dataset_crab_path = (
                        crabconfigarea / dataset_crab.General.requestName
                    )
                    args["crabconfigs"][k][dt_period][dataset_type][dkey] = (
                        str(dataset_crab_path) + ".py"
                    )
                    # TODO: introduce a check for existence and checksum check
                    print(
                        f'Creating crab config: {args["crabconfigs"][k][dt_period][dataset_type][dkey]}'
                    )
                    with open(
                        args["crabconfigs"][k][dt_period][dataset_type][dkey], "w"
                    ) as out_crab:
                        out_crab.write(str(dataset_crab))

    return args


if __name__ == "__main__":
    args = initialize(parse_args())
    args = prepare(args)
