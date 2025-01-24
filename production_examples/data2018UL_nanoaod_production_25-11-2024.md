# NanoAOD production campaign for 2018 data

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](../configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](../configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`configuration/configuration/datasets_miniaod_htt_data_2018UL.yaml`](../configuration/datasets_miniaod_htt_data_2018UL.yaml)
* crab config template: [`crab_configuration/crab_template.py`](../crab_configuration/crab_template.py)
* CMSSW release: CMSSW_13_0_21

## Creation of CMSSW and Crab configs call

General call:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/htt_data_crab_nanoaod_submission_25-11-2024_prodreleasev12/ \
  --datasets configuration/datasets_miniaod_htt_data_2018UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 500 --publication --splitting EventAwareLumiBased --unitsPerJob 1000000 --maxJobRuntimeMin 900
```

### Adaptations during production campaign

For `Tau_2018D` and `EGamma_2018D` the individual events in some inputs seemed to be very packed. Furthermore, some jobs at sites claimed to have processed all events, but a fraction of events were missing. Therefore, changed the setup for these datasets to blacklisting and whitlisting some sites. Most reliable setup is really to whitelist T1_DE_KIT, provided that the inputs are placed there. In that case, jobs can also run at T2_DE_RWTH and at T2_DE_DESY:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/htt_data_crab_nanoaod_submission_25-11-2024_prodreleasev12_filebased/ \
  --datasets configuration/datasets_miniaod_htt_data_2018UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 500 --publication --splitting FileBased --unitsPerJob 5 --maxJobRuntimeMin 900 \
  --siteBlacklist T1_US_FNAL T2_US_* --siteWhitelist T1_DE_KIT
```

 Consider switching to FileBased processing as an alternative, if needed.

## Managing of crab tasks call

Initial calls will be presented in the following, which can be adapted further for resubmission supplemented with available resubmission options (see `./create_configs.py --help`).

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/htt_data_crab_nanoaod_submission_25-11-2024_prodreleasev12*/crabconfigs/*.py
```

## Results

The finished production campaign can be seen at CMS Grafana:

https://monit-grafana.cern.ch/goto/FpS-myIHR?orgId=11

The resulting datasets are (accessible via DAS webpage or `dasgoclient`, using `prod/phys03` DBS instance):

```bash
/MuonEG/aakhmets-data_2018UL_muonegamma_MuonEG_Run2018A_1732626664-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2018UL_muonegamma_MuonEG_Run2018B_1732626664-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2018UL_muonegamma_MuonEG_Run2018C_1732626664-00000000000000000000000000000000/USER
/MuonEG/aakhmets-data_2018UL_muonegamma_MuonEG_Run2018D_1732626664-00000000000000000000000000000000/USER
/EGamma/aakhmets-data_2018UL_singleelectron_EGamma_Run2018A_1732626664-00000000000000000000000000000000/USER
/EGamma/aakhmets-data_2018UL_singleelectron_EGamma_Run2018B_1732626664-00000000000000000000000000000000/USER
/EGamma/aakhmets-data_2018UL_singleelectron_EGamma_Run2018C_1732626664-00000000000000000000000000000000/USER
/EGamma/aakhmets-data_2018UL_singleelectron_EGamma_Run2018D_1734519534-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2018UL_tau_Tau_Run2018A_1732626664-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2018UL_tau_Tau_Run2018B_1732626664-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2018UL_tau_Tau_Run2018C_1732626664-00000000000000000000000000000000/USER
/Tau/aakhmets-data_2018UL_tau_Tau_Run2018D_1734106865-00000000000000000000000000000000/USER
```