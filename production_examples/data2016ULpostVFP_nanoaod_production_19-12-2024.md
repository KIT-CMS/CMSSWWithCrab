# NanoAOD production campaign to test the tool

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](../configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](../configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`configuration/configuration/datasets_miniaod_htt_data_2016ULpostVFP.yaml`](../configuration/datasets_miniaod_htt_data_2016ULpostVFP.yaml)
* crab config template: [`crab_configuration/crab_template.py`](../crab_configuration/crab_template.py)
* CMSSW release: CMSSW_13_0_21

## Further preparation:

Moved the required datasets to T1_DE_KIT_Disk storage to make sure, that they can be processed at German sites.

## Creation of CMSSW and Crab configs call

General call:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/htt_data_2016_crab_nanoaod_submission_19-12-2024_prodreleasev12/ \
  --datasets configuration/datasets_miniaod_htt_data_2016ULpostVFP.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 4 --numCores 4 \
  --maxMemoryMBperCore 750 --publication --splitting EventAwareLumiBased --unitsPerJob 500000 --maxJobRuntimeMin 900
```

## Managing of crab tasks call

Initial calls will be presented in the following, which can be adapted further for resubmission supplemented with available resubmission options (see `./create_configs.py --help`). Extend with `--nworkers` greater than 0 to enable the status check and potential resubmission.

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/htt_data_2016_crab_nanoaod_submission_19-12-2024_prodreleasev12/crabconfigs/*postVFP*.py
```

## Results

The finished production campaign can be seen at CMS Grafana:

https://monit-grafana.cern.ch/goto/LZ3SgMNNR?orgId=11

The resulting datasets are (accessible via DAS webpage or `dasgoclient`, using `prod/phys03` DBS instance):

```bash
/MuonEG/aakhmets-data_2016ULpostVFP_muonegamma_MuonEG_Run2016F_1734617846-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2016ULpostVFP_muonegamma_MuonEG_Run2016G_1734617846-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2016ULpostVFP_muonegamma_MuonEG_Run2016H_1734617846-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2016ULpostVFP_singleelectron_SingleElectron_Run2016F_1735028768-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2016ULpostVFP_singleelectron_SingleElectron_Run2016G_1734617846-00000000000000000000000000000000/USER
/SingleElectron/aakhmets-data_2016ULpostVFP_singleelectron_SingleElectron_Run2016H_1734617846-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2016ULpostVFP_singlemuon_SingleMuon_Run2016F_1734617846-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2016ULpostVFP_singlemuon_SingleMuon_Run2016G_1734617846-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2016ULpostVFP_singlemuon_SingleMuon_Run2016H_1734617846-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2016ULpostVFP_tau_Tau_Run2016F_1734617846-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2016ULpostVFP_tau_Tau_Run2016G_1734617846-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2016ULpostVFP_tau_Tau_Run2016H_1734617846-00000000000000000000000000000000/USER
```