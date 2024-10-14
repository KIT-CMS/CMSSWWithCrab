# CMSSWWithCrab
Lightweight setup to submit CMSSW jobs with Crab for large-scale production

## Prerequisites

A valid `CMSSW` checkout and environment. Can be obtained via:

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh;
cmsrel CMSSW_${RELEASE_NUMBER}
cd CMSSW_${RELEASE_NUMBER}/src
cmsenv
```

For `${RELEASE_NUMBER}` as of now, the latest one would be `14_2_0_pre2`. Feel free to choose `CMSSW` version which suits you most.

Ability to source `crab3` software and create a VOMS proxy certificate via:

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
voms-proxy-init --valid 192:00:00 --voms cms:/dcms --rfc
```

Checkout of this setup:

```bash
git clone git@github.com:KIT-CMS/CMSSWWithCrab.git
```

## Creation of CMSSW and Crab3 configs for CMSSW dataset production

Considering the example of nanoAOD production.

The script [`create_configs.py`](create_configs.py) creates `cmsRun` configs via `cmsDriver.py`, which are processed further
to create [`crab3`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab) configs per dataset to process. The script needs the following information in `.yaml` format:

* Conditions for processing CMS data. Example: [`configuration/conditions.yaml`](configuration/conditions.yaml)
* CMSSW specific settings to be passed to cmsDriver commands. Example: [`configuration/cmsdriver_nanoaod_specifics.yaml`](configuration/cmsdriver_nanoaod_specifics.yaml)
* Datasets to process. Example: [`configuration/datasets_miniaod_boostedhtt.yaml`](configuration/datasets_miniaod_boostedhtt.yaml)

In addition, general `crab3` configuration, which is provided via [`crab_configuration/crab_template.py`](crab_configuration/crab_template.py)

Please get familiar with these files and their structure to be able to construct corresponding files for your use-case.

### Some considerations for `cmsRun` configs

Often it might make sense to run `cmsRun` multi-threaded (and even with different number of streams). To this up properly, please use the `--nThreads` and `--nStreams`
options of [`create_configs.py`](create_configs.py), which are passed to `cmsRun`. If doing so for the case of grid jobs, you need to take into account,
how many threads/streams are usually used within the CMS grid environment. Suggestion: please use at most 4 cores, since these would better fit in into CMSW job containers,
which are designed for jobs wiht 4 or 8 threads.

Furthermore, it might be, that depending on these settings, the memory consumption of the job significantly changes.
Feel free to set these numbers differently, e.g. `--nThreads 4`, but `--nStreams 2`, or even `--nStreams 1`.

### Some considerations for `crab3` configs

After creating the `cmsRun` configs, you should further consider the options available for
[`crab3`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab#Documentation_for_beginner_users) configuration.
For [`create_configs.py`](create_configs.py), the following were found of importance and are added explicitly to the script to be passed to the configuration files:

* `--numCores` regulates the number of requested CPUs. Please choose that consistently with the `cmsRun` settings for `--nThreads` and `--nStreams` to avoid overuse of requested resources.
* `--maxMemoryMBperCore` is what you would like to request for memory per CPU for your job. This number is then multiplied by what was configured in `--numCores`, and is passed to `--maxMemoryMB` from crab.
* `--splitting` and `--unitsPerJob` define, how your input data is distributed among the jobs. In most cases, `Automatic` splitting is a good choice, and `--unitsPerJob` represent in that case the desired job runtime. Please get familiar with this setting
* `--publication` is a flag, which allows to publish your output data in CMS DBS under `phys03` instance. This makes it much simpler to collect lists of output files. Feel free to use that for your actual production campaigns.
