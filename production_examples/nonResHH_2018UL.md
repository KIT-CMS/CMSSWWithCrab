# NanoAOD production for non resonant HH production - mc signals 

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](../configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](../configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`configuration/datasets_miniaod_nonResHH_2018UL.yaml`](../configuration/datasets_miniaod_nonResHH_2018UL.yaml)
* crab config template: [`crab_configuration/crab_template.py`](../crab_configuration/crab_template.py)
* CMSSW release: CMSSW_13_0_21

## Creation of CMSSW and Crab configs call

### mc:

Decided to go for an `EventAwareLumiBased` splitting with 1M events to be processed.
Chose 15 hours as maximum runtime and 4 GB as maximum memory.

```bash
./create_configs.py --work-directory /eos/user/s/sdaigler/work/nonResHH_2018UL_29-11-2024_prodreleasev12/ \
  --datasets configuration/datasets_miniaod_nonResHH_2018UL.yaml \
  --conditions configuration/conditions.yaml \
  --cmsdriver configuration/cmsdriver_nanoaod_specifics.yaml \
  --nThreads 8 --numCores 8 \
  --maxMemoryMBperCore 500 --publication --splitting EventAwareLumiBased --unitsPerJob 1000000 --maxJobRuntimeMin 900
```

## Managing of crab tasks call

### mc:

```bash
./crab_manager.py --crab-config-pattern \
  /eos/user/s/sdaigler/work/nonResHH_2018UL_29-11-2024_prodreleasev12/crabconfigs/*.py --nworkers 13
```

Resubmitted Tasks manually.

```bash
 crab resubmit -d /eos/user/s/sdaigler/work/nonResHH_2018UL_29-11-2024_prodreleasev12/crab/crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_SM
```

## Results

The finished production campaign can be seen at CMS Grafana:

https://monit-grafana.cern.ch/goto/h1HmEmIHR?orgId=11

The resulting datasets are (accessible via DAS webpage or `dasgoclient`, using `prod/phys03` DBS instance):

```bash
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_SM_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_SM_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_1_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_1_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_2_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_2_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_3_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_3_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_4_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_4_1732876480-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_5_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_5_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_6_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_6_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_7_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_7_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_8_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_8_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_9_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_9_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_10_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_10_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_11_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_11_1733315721-00000000000000000000000000000000/USER
/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_12_13TeV-madgraph-pythia8/sdaigler-mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_12_1733315721-00000000000000000000000000000000/USER
```
