# NanoAOD production campaign to test the tool

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](../configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](../configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`configuration/configuration/datasets_miniaod_htt_data_2017UL.yaml`](../configuration/datasets_miniaod_htt_data_2017UL.yaml)
* crab config template: [`crab_configuration/crab_template.py`](../crab_configuration/crab_template.py)
* CMSSW release: CMSSW_13_0_21

## Further preparation:

Moved the required dataset to T1_DE_KIT_Disk storage to make sure, that they can be processed at German sites.

## Creation of CMSSW and Crab configs call

General call:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/htt_data_2017_crab_nanoaod_submission_16-12-2024_prodreleasev12/ \
  --datasets configuration/datasets_miniaod_htt_data_2017UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 4 --numCores 4 \
  --maxMemoryMBperCore 750 --publication --splitting EventAwareLumiBased --unitsPerJob 250000 --maxJobRuntimeMin 900
```

### Adaptations during production campaign

For `SingleMuon_2017C` some jobs claimed to have processed all events, but a fraction of events were missing. Therefore, changed the setup for this dataset to whitelist T1_DE_KIT only and run with 1 file per job. Provided, that the files are at T1_DE_KIT, jobs can also run at T2_DE_RWTH and at T2_DE_DESY:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/htt_data_2017_crab_nanoaod_submission_16-12-2024_prodreleasev12_filebased/ \
  --datasets configuration/datasets_miniaod_htt_data_2017UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 4 --numCores 4 \
  --maxMemoryMBperCore 750 --publication --splitting FileBased --unitsPerJob 1 --maxJobRuntimeMin 360 \
  --siteWhitelist T1_DE_KIT
```

 Consider switching to FileBased processing as an alternative, if needed, in particular in case of inconsistent number of events between input and output.

## Managing of crab tasks call

Initial calls will be presented in the following, which can be adapted further for resubmission supplemented with available resubmission options (see `./create_configs.py --help`). Extend with `--nworkers` greater than 0 to enable the status check and potential resubmission.

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/htt_data_2017_crab_nanoaod_submission_16-12-2024_prodreleasev12*/crabconfigs/*.py
```

## Results

The finished production campaign can be seen at CMS Grafana:

https://monit-grafana.cern.ch/goto/RU7RI9IHR?orgId=11

The resulting datasets are (accessible via DAS webpage or `dasgoclient`, using `prod/phys03` DBS instance):

```bash
/MuonEG/aakhmets-data_2017UL_muonegamma_MuonEG_Run2017B_1734360140-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2017UL_muonegamma_MuonEG_Run2017C_1734360140-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2017UL_muonegamma_MuonEG_Run2017D_1734360140-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2017UL_muonegamma_MuonEG_Run2017E_1734360140-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2017UL_muonegamma_MuonEG_Run2017F_1734360140-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2017UL_singleelectron_SingleElectron_Run2017B_1734360140-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2017UL_singleelectron_SingleElectron_Run2017C_1734360140-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2017UL_singleelectron_SingleElectron_Run2017D_1734360140-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2017UL_singleelectron_SingleElectron_Run2017E_1734360140-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2017UL_singleelectron_SingleElectron_Run2017F_1734360140-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2017UL_singlemuon_SingleMuon_Run2017B_1734360140-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2017UL_singlemuon_SingleMuon_Run2017C_1734866484-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2017UL_singlemuon_SingleMuon_Run2017D_1734360140-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2017UL_singlemuon_SingleMuon_Run2017E_1734360140-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2017UL_singlemuon_SingleMuon_Run2017F_1734360140-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2017UL_tau_Tau_Run2017B_1734360140-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2017UL_tau_Tau_Run2017C_1734360140-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2017UL_tau_Tau_Run2017D_1734360140-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2017UL_tau_Tau_Run2017E_1734360140-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2017UL_tau_Tau_Run2017F_1734360140-00000000000000000000000000000000/USER
```