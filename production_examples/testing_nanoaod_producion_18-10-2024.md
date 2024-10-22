# NanoAOD production campaign to test the tool

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`configuration/datasets_miniaod_boostedhtt.yaml`](configuration/datasets_miniaod_boostedhtt.yaml)
* crab config template: [`crab_configuration/crab_template.py`](crab_configuration/crab_template.py)
* CMSSW release: ~~CMSSW_14_2_0_pre2~~ (**memory leak!!!**) CMSSW_13_0_21

<details><summary>Deprecated due to CMSSW_14_2_0_pre2 issues</summary>

## Creation of CMSSW and Crab configs call

### data:

Tested locally on one input file with about 35k events, and there weren't any memory leaks visible.
Something like 2.5 GB memory was used usually with 8 threads and 8 streams.
Runtime for this was around half an hour. Used these values to have a good estimate for the `crab3` jobs.

Final call:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_data/ \
  --datasets configuration/datasets_miniaod_boostedhtt.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 1000 --publication --splitting FileBased --unitsPerJob 15 --maxJobRuntimeMin 1250
```

### mc:

Tested locally on one input file with about 30k events, and unfortunately, there was a memory leak.
Something like 15 GB memory was used with 8 threads and 8 streams.
Decided to go for an `EventAwareLumiBased` splitting with 10k events to be processed.
This reduces the runtime to something like an hour and memory to about 5 GB.
To be safe, choosing 2 hours as maximum runtime and 10 GB as maximum memory.
This will lead to a lot of and extremely small output files.
To be checked, whether this impacts the performance later on when these datasets are used for analysis.

Final call:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_mc/ \
  --datasets configuration/datasets_miniaod_boostedhtt.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 1250 --publication --splitting EventAwareLumiBased --unitsPerJob 10000 --maxJobRuntimeMin 120
```

## Managing of crab tasks call

Initial calls will be presented in the following, which can be adapted further for resubmission by adding at least one of the two options `--maxmemory` and `--maxjobruntime`-

### data:

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_data/crabconfigs/data_2018UL_singlemuon_SingleMuon_Run2018*.py
```

### mc:

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_mc/crabconfigs/mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-250To400.py \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_mc/crabconfigs/mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-400To650.py \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_mc/crabconfigs/mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-650ToInf.py \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_mc/crabconfigs/mc_2018UL_ttbar_TTToSemiLeptonic.py \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024_mc/crabconfigs/mc_2018UL_wjets_WJetsToLNu.py
```

</details>

## Creation of CMSSW and Crab configs call

Tested locally on one input file with about 48k events, and there weren't any memory leaks visible.
Something like 2.5 GB memory was used usually with 8 threads and 8 streams.
Runtime for this was around half an hour. Used these values to have a good estimate for the `crab3` jobs.

Final call:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024/ \
  --datasets configuration/datasets_miniaod_boostedhtt.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 1000 --publication --splitting EventAwareLumiBased --unitsPerJob 1000000 --maxJobRuntimeMin 900
```

## Managing of crab tasks call

Initial calls will be presented in the following, which can be adapted further for resubmission supplemented with available resubmission options (see `./create_configs.py --help`).

### data:

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/test_crab_nanoaod_submission_18-10-2024/crabconfigs/*.py
```