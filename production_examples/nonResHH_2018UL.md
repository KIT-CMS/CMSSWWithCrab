# NanoAOD production for non resonant HH production - mc signals 

## Used configuration and setup:

* conditions: [`configuration/conditions.yaml`](../configuration/conditions.yaml)
* cmsdriver settings for nanoAOD: [`configuration/cmsdriver_nanoaod_specifics.yaml`](../configuration/cmsdriver_nanoaod_specifics.yaml)
* datasets: [`../configuration/datasets_miniaod_nonResHH_2018UL.yaml`](../configuration/datasets_miniaod_nonResHH_2018UL.yaml)
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

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123808%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_SM&from=1733315888000&to=1734086413348

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123705%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_1&from=1733315825000&to=1734086427884

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123727%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_2&from=1733315847000&to=1734086452621

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123732%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_3&from=1733315852000&to=1734086460275

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241129_111400%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_4&from=1732878840000&to=1734086467779

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123739%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_5&from=1733315859000&to=1734086475346

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123743%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_6&from=1733315863000&to=1734086487875

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123753%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_7&from=1733315873000&to=1734086497388

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123758%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_8&from=1733315878000&to=1734086506867

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123804%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_9&from=1733315884000&to=1734086515411

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123711%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_10&from=1733315831000&to=1734086522714

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123716%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_11&from=1733315836000&to=1734086530224

https://monit-grafana.cern.ch/d/cmsTMDetail/cms-task-monitoring-task-view?orgId=11&var-user=sdaigler&var-task=241204_123722%3Asdaigler_crab_mc_2018UL_gghh2b2tau_GluGluToHHTo2B2Tau_Node_12&from=1733315842000&to=1734086537892


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