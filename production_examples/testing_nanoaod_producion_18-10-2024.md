# NanoAOD production campaign to test the tool

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](../(configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](../configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`configuration/datasets_miniaod_boostedhtt_2018UL.yaml`](../configuration/datasets_miniaod_boostedhtt_2018UL.yaml)
* crab config template: [`crab_configuration/crab_template.py`](../crab_configuration/crab_template.py)
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
  --datasets configuration/datasets_miniaod_boostedhtt_2018UL.yaml \
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
  --datasets configuration/datasets_miniaod_boostedhtt_2018UL.yaml \
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
./create_configs.py --work-directory /ceph/$(whoami)/test_crab_nanoaod_submission_21-10-2024_prodreleasev12/ \
  --datasets configuration/datasets_miniaod_boostedhtt_2018UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 500 --publication --splitting EventAwareLumiBased --unitsPerJob 1000000 --maxJobRuntimeMin 900
```

### Adaptions during production campaign

Due to some of the tasks being not processed well, changed the setup for a few larger datasets to:

```bash
./create_configs.py --work-directory /ceph/$(whoami)/test_crab_nanoaod_submission_21-10-2024_prodreleasev12_filebased/ \
  --datasets configuration/datasets_miniaod_boostedhtt_2018UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 500 --publication --splitting FileBased --unitsPerJob 5 --maxJobRuntimeMin 900
```

 Consider switching to FileBased processing as an alternative, if needed.

## Managing of crab tasks call

Initial calls will be presented in the following, which can be adapted further for resubmission supplemented with available resubmission options (see `./create_configs.py --help`).

```bash
./crab_manager.py --crab-config-pattern \
  /ceph/$(whoami)/test_crab_nanoaod_submission_21-10-2024_prodreleasev12*/crabconfigs/*.py
```

## Results

The finished production campaign can be seen at CMS Grafana:

https://monit-grafana.cern.ch/goto/h4P2U-ZNg?orgId=11

The resulting datasets are (accessible via DAS webpage or `dasgoclient`, using `prod/phys03` DBS instance):

```bash
/SingleMuon/aakhmets-data_2018UL_singlemuon_SingleMuon_Run2018A_1729863731-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2018UL_singlemuon_SingleMuon_Run2018B_1729599421-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2018UL_singlemuon_SingleMuon_Run2018C_1730057166-00000000000000000000000000000000/USER
/SingleMuon/aakhmets-data_2018UL_singlemuon_SingleMuon_Run2018D_1729599421-00000000000000000000000000000000/USER
/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_diboson_WZTo2Q2L_1729599421-00000000000000000000000000000000/USER
/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_diboson_WZTo3LNu_1729599421-00000000000000000000000000000000/USER
/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_diboson_ZZTo2Q2L_1729599421-00000000000000000000000000000000/USER
/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/aakhmets-mc_2018UL_diboson_ZZTo4L_1729599421-00000000000000000000000000000000/USER
/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-100To250_1729599421-00000000000000000000000000000000/USER
/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-250To400_1729599421-00000000000000000000000000000000/USER
/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-400To650_1729599421-00000000000000000000000000000000/USER
/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/aakhmets-mc_2018UL_dy_DYJetsToLL_LHEFilterPtZ-650ToInf_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_1000to1400_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_1400to1800_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_170to300_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_1800to2400_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_2400to3200_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_300to470_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_3200toInf_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_470to600_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_600to800_1729599421-00000000000000000000000000000000/USER
/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/aakhmets-mc_2018UL_qcd_QCD_Pt_800to1000_1729599421-00000000000000000000000000000000/USER
/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/aakhmets-mc_2018UL_singletop_ST_t-channel_antitop_4f_InclusiveDecays_1729599421-00000000000000000000000000000000/USER
/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/aakhmets-mc_2018UL_singletop_ST_t-channel_top_4f_InclusiveDecays_1729599421-00000000000000000000000000000000/USER
/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/aakhmets-mc_2018UL_singletop_ST_tW_antitop_5f_inclusiveDecays_1729599421-00000000000000000000000000000000/USER
/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/aakhmets-mc_2018UL_singletop_ST_tW_top_5f_inclusiveDecays_1729599421-00000000000000000000000000000000/USER
/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/aakhmets-mc_2018UL_ttbar_TTTo2L2Nu_1729599001-00000000000000000000000000000000/USER
/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/aakhmets-mc_2018UL_ttbar_TTToHadronic_1729599001-00000000000000000000000000000000/USER
/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/aakhmets-mc_2018UL_ttbar_TTToSemiLeptonic_1729530171-00000000000000000000000000000000/USER
/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/aakhmets-mc_2018UL_wjets_WJetsToLNu_1729599421-00000000000000000000000000000000/USER
```