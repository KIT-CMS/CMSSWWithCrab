#! /usr/bin/env python3

import yaml
import argparse
import pathlib
import subprocess
import shlex
import copy
import datetime

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
    parser.add_argument(
        "--work-directory", required=True, help="Path to the main work directory"
    )
    parser.add_argument(
        "--datasets", required=True, help="Path to the dataset configuration .yaml file"
    )

    ## Optional arguments

    # CMSSW configuration group
    cmssw = parser.add_argument_group(
        "CMSSW", "Configuration related to CMSSW settings to run a cmsRun config"
    )

    ## Necessary arguments
    cmssw.add_argument(
        "--conditions",
        required=True,
        help="Path to the conditions configuration .yaml file",
    )
    cmssw.add_argument(
        "--cmsdriver",
        required=True,
        help="Path to the cmsdriver configuration .yaml file",
    )
    cmssw.add_argument(
        "--nThreads",
        type=int,
        default=1,
        help="Number of threads to be used for the cmsRun config",
    )
    cmssw.add_argument(
        "--nStreams",
        type=int,
        default=0,
        help="Number of streams to be used for the cmsRun config. If set to 0, nThreads will be taken by cmsRun.",
    )

    # Crab configuration group
    crab = parser.add_argument_group(
        "crab3", "Configuration related to crab3 settings to submit a crab task"
    )

    ## Optional arguments
    crab.add_argument(
        "--numCores",
        type=int,
        default=1,
        help="Number of Cores used by crab for the job",
    )
    crab.add_argument(
        "--maxMemoryMBperCore",
        type=int,
        default=2000,
        help="Maximum memory in MB to be used by the crab job per core",
    )
    crab.add_argument(
        "--maxJobRuntimeMin",
        type=int,
        default=720,
        help="Maximum runtime expected for the job im minutes",
    )
    crab.add_argument(
        "--publication",
        action="store_true",
        help="Flag to decide, whether to publish crab output dataset",
    )
    crab.add_argument(
        "--splitting",
        choices=["Automatic", "FileBased", "LumiBased", "EventAwareLumiBased"],
        default="Automatic",
        help="Choice of splitting of the task into jobs.",
    )
    crab.add_argument(
        "--unitsPerJob",
        type=int,
        default=720,
        help="Rough number of files (FileBased), luminosity sections (LumiBased), or events (EventAwareLumiBased) to have per job, depending on the corresponding splitting. In case of Automatic splitting: target runtime in minutes with a minimum of 180.",
    )
    crab.add_argument(
        "--siteWhitelist",
        nargs="*",
        help="List of sites to exclusively run your jobs on.",
    )
    crab.add_argument(
        "--siteBlacklist",
        nargs="*",
        help="List of sites to avoid running your jobs there.",
    )

    return parser.parse_args()


def initialize(args):
    args_dict = vars(args)
    args_dict["datasets"] = yaml.safe_load(open(args_dict["datasets"], "r"))
    args_dict["conditions"] = yaml.safe_load(open(args_dict["conditions"], "r"))
    args_dict["cmsdriver"] = yaml.safe_load(open(args_dict["cmsdriver"], "r"))
    args_dict["crab"] = config
    args_dict["timestamp"] = str(int(datetime.datetime.now().timestamp()))
    return args_dict


def prepare(args):
    # Ensure, that work directory exists
    work_directory = pathlib.Path(args["work_directory"])
    work_directory.mkdir(mode=0o755, parents=True, exist_ok=True)

    # Prepare cmsDriver commands and create cmsRun configs
    cmsdriver_directory = work_directory / "cmsdriver"
    cmsdriver_directory.mkdir(mode=0o755, parents=True, exist_ok=True)

    cmsdriver_keys = set(args["cmsdriver"].keys())
    conditions_keys = set(args["conditions"].keys())
    if cmsdriver_keys != conditions_keys:
        print(
            f"Error: expecting keys for cmsdriver keys {cmsdriver_keys} to be the same as condition keys {conditions_keys}. This is not the case"
        )
        exit(1)

    cmsdriver_commands = []
    for k, cmsdriverspecs in args["cmsdriver"].items():
        for dt_period, configuration in args["conditions"][k].items():
            cmsrundir = cmsdriver_directory / str(dt_period)
            cmsrundir.mkdir(mode=0o755, parents=True, exist_ok=True)
            cmsrun = cmsrundir / cmsdriverspecs["python_filename"]
            args["conditions"][k][dt_period]["cmsrun"] = cmsrun
            command = f'cmsDriver.py {cmsdriverspecs["type"]} --{k} --filein file:{cmsdriverspecs["filein"]} --fileout {cmsdriverspecs["fileout"]} --step {cmsdriverspecs["step"]} --eventcontent {cmsdriverspecs["eventcontent"]} --datatier {cmsdriverspecs["datatier"]} --python_filename {str(cmsrun)} --conditions {configuration["globaltag"]} --era {configuration["era"]} --no_exec --nThreads {args["nThreads"]} --nStreams {args["nStreams"]}'
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
                    dataset_crab.JobType.psetName = str(
                        args["conditions"][k][dt_period]["cmsrun"]
                    )
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
