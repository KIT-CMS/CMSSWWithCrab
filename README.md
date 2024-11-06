# CMSSWWithCrab
Lightweight setup to submit CMSSW jobs with Crab for large-scale production

In the following, you will find some general description on the package.
For explicit production examples, please have a look into the [production_examples](production_examples) folder.

## Prerequisites

A valid `CMSSW` checkout and environment. Can be obtained via:

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh;
cmsrel CMSSW_${RELEASE_NUMBER}
cd CMSSW_${RELEASE_NUMBER}/src
cmsenv
```

For `${RELEASE_NUMBER}` as of now, the latest **stable** one would be ~~`14_2_0_pre2`~~ (has a memory leak...) `13_0_21`.
Feel free to choose `CMSSW` version which suits you most.

Ability to source `crab3` software and create a VOMS proxy certificate via:

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
export CRAB3_CACHE_FILE=/dev/null
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
how many threads/streams are usually used within the CMS grid environment. Suggestion: please use at 8 cores, since these would better fit in into CMSW job containers,
which are designed for jobs with up to 8 threads.

Furthermore, it might be, that depending on these settings, the memory consumption of the job significantly changes.
Feel free to set these numbers differently, e.g. `--nThreads 4`, but `--nStreams 2`, or even `--nStreams 1`.

You are strongly adviced to test the `cmsRun` config locally on an representative input file, check both the runtime and memory consumption, and project
the outcome to proper requirements for `crab3` config.

It might well be, that there are differences in performance and resource consumption between processing recorded data samples, or simulated samples.
In consequence, please test these two main use-cases separately from each other.

One example of an issue would be a memory leak appearing e.g. only for simulated datasets. Please check in such cases, whether a more suitable/stable CMSSW release
can be used without any memory leak.

### Some considerations for `crab3` configs

After creating the `cmsRun` configs, you should further consider the options available for
[`crab3`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab#Documentation_for_beginner_users) configuration.
For [`create_configs.py`](create_configs.py), the following were found of importance and are added explicitly to the script to be passed to the configuration files:

* `--numCores` regulates the number of requested CPUs. Please choose that consistently with the `cmsRun` settings for `--nThreads` and `--nStreams` to avoid overuse of requested resources.
* `--maxMemoryMBperCore` is what you would like to request for memory per CPU for your job. This number is then multiplied by what was configured in `--numCores`, and is passed to `--maxMemoryMB` from crab.
* `--splitting` and `--unitsPerJob` define, how your input data is distributed among the jobs. Usually, `Automatic` splitting is a good choice, and `--unitsPerJob` represent in that case the desired job runtime - try to target something below 24 hours, e.g. 1250 minutes. Please get familiar with this setting. However, since testing a `cmsRun` config locall works easiest with a specific number of files or events, you might want to consider `FileBased` or `EventAwareLumiBased` splitting to have more control over the runtime and memory consumption of your jobs. This might prevent too frequent resubmissions of jobs.
* `maxJobRuntimeMin` defines the maximum expected runtime of your jobs and is passed to crab configuration. Jobs with larger runtimes will be potentially aborted and fail, so try to estimate this number properly.
* `--publication` is a flag, which allows to publish your output data in CMS DBS under `phys03` instance. This makes it much simpler to collect lists of output files. Feel free to use that for your actual production campaigns. In case you choose to publish your dataset, it obtains a custom `outputDatasetTag` used in the dataset name, constructed from `requestName` and the timestamp integer at the time your are running `./create_configs.py`. This ensures, that datasets have (more or less) unique names. In that context, please avoid submitting a `crab3` task, then deleting the task directory after some time, and then, resubmitting the same task with the same configuation again. That might lead to duplication of content of published datasets. At each task submission attempt, please ensure, that you use a new configuration (e.g. by re-rerunning `./create_configs.py`).
* `--siteWhitelist` and `--siteBlacklist` can be used to have (come) control on which sites are used to run there your jobs. Under ideal circumstances, it would be good to use all available sites where the input files are placed, since restricting to only a few sites via whitelist might lead to a bad task throughput, such that you would need to wait quite long for a production campaign to finish. On the other hand, there might be bad sites with problems, or even with corrupt files which look OK on the outside (yes, that might happen, too...). For such cases, a blacklist of sites can help.

Furthermore, you have to consider a few server-sided restrictions/constraints for jobs running on the grid:

* Usually, jobs are allowed to use up to 2.5GB per core. Submission of jobs with high requirements than that might be refused
* Increasing the runtime significantly over 24h might lead to lack of available and matching resources. So try to keep the runtimes to be below 24h, e.g. at 12h or 15h.
* Per `crab3` task, you are only allowed to have a maximum of 10k jobs. So try to keep the work per job at a large enough amount, e.g. the number of events to process should be kept high enough.

These restrictions have to be taken into account especially, when you encounter memory leaks.
These usually lead to memory overuse, and in consequence, to failing jobs, or a trend towards small amount of work per job.
The latter consequence is a killer for processing of large datasets.
A way out of that might be older CMSSW releases, which have proven to be fine for official large-scale productions.

### Example call:

```bash
./create_configs.py --work-directory ~/crab_work_dir \
  --datasets configuration/datasets_miniaod_boostedhtt.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --numCores 4 --nThreads 4 --nStreams 2 --maxMemoryMBperCore 1250 --publication
```
## Managing multiple crab3 tasks

After all required `crab3` configuration files were created as expected, you can proceed managing their submission.
For that purpose, the script [`crab_manager.py`](crab_manager.py) was designed. It processes a list of `crab3` configs, with a number of workers running asynchronously in parallel, specified by `--nworkers`. The parallelization is based on a queue concept. The workflow is as follows:

1) After getting a `crab3` config from the submissionqueue, and in case the task directory assigned to this `crab3` config does not exist, the submission of this task is executed. After that, the task directory is available and properly set. To make sure, that there are no problems related to parallel processing, the submission is done sequentially for the configs from the submission queue. After the submission was performed, the configuration is passed further to the status queue to process it with the remaining workflow, using multiple workers.
2) For a properly created task directory, the status is queried regularly, checking the number of all, intermediate, (idle and running), finished, failed, and published jobs.
3) In case failed jobs are encountered, and there aren't any intermediate jobs left, a resubmission attempt could be initiated, if at least one of the options `--maxmemory` and `--maxjobruntime` were specified, when starting `./crab_manager.py`. Please be careful when resubmitting to avoid too many attempts by paying attention to specify good values for these two options. Furthermore, `--siteblacklist` and `--sitewhitelist` can be used to have a better control on sites do resubmit the jobs to.
4) If everything was processed successfully, it is expected, that numbers of all, finished, and published jobs are equal. In that, case the name of the published dataset is printed, and the `crab3` task is considered as done.
5) If the queue is not empty, the next `crab3` config is taken by the worker to be processed.

### Example call:

```bash
./crab_manager.py --crab-config-pattern ~/crab_work_dir/crabconfigs/data_2018UL_singlemuon_SingleMuon_Run2018*.py \
  --maxjobruntime 1300 \
  --maxmemory 8000
```

## Useful notes

* very good monitoring page for crab tasks: https://monit-grafana.cern.ch/d/15468761344/personal-tasks-monitoring-globalview?orgId=11&from=now-1h&to=now. Try to adjust the settings according to your CERN account name, and the time period of interest.
