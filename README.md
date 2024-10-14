# CMSSWWithCrab
Lightweight setup to submit CMSSW jobs with Crab for large-scale production

## Creation of CMSSW and Crab3 configs for CMSSW dataset production

Considering the example of nanoAOD production.

The script [`create_configs.py`](create_configs.py) creates `cmsRun` configs via `cmsDriver.py`, which are processed further to create [`crab3`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab) configs per dataset to process. The script needs the following information in `.yaml` format:

* Conditions for processing CMS data. Example: [`configuration/conditions.yaml`](configuration/conditions.yaml)
* CMSSW specific settings to be passed to cmsDriver commands. Example: [`configuration/cmsdriver_nanoaod_specifics.yaml`](configuration/cmsdriver_nanoaod_specifics.yaml)
* Datasets to process. Example: [`configuration/datasets_miniaod_boostedhtt.yaml`](configuration/datasets_miniaod_boostedhtt.yaml)
* General `crab3` configuration, which is provided via [`crab_configuration/crab_template.py`](crab_configuration/crab_template.py)
