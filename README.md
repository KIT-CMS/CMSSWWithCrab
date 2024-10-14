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

The script [`create_configs.py`](create_configs.py) creates `cmsRun` configs via `cmsDriver.py`, which are processed further to create [`crab3`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab) configs per dataset to process. The script needs the following information in `.yaml` format:

* Conditions for processing CMS data. Example: [`configuration/conditions.yaml`](configuration/conditions.yaml)
* CMSSW specific settings to be passed to cmsDriver commands. Example: [`configuration/cmsdriver_nanoaod_specifics.yaml`](configuration/cmsdriver_nanoaod_specifics.yaml)
* Datasets to process. Example: [`configuration/datasets_miniaod_boostedhtt.yaml`](configuration/datasets_miniaod_boostedhtt.yaml)

In addition, general `crab3` configuration, which is provided via [`crab_configuration/crab_template.py`](crab_configuration/crab_template.py)

Please get familiar with these files and their structure to be able to construct corresponding files for your use-case.

### Some considerations for `cmsRun` configs

### Some considerations for `crab3` configs
