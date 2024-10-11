# General Twiki for crab: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab
# Structure of a crab configuration file: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
import CRABClient
from CRABClient.UserUtilities import config

config = config()

# General section
config.General.instance = "prod"

# JobType section
config.JobType.pluginName = "Analysis"

# Data section

# Site section
config.Site.storageSite = "T1_DE_KIT"

# User section
config.voGroup = "/cms/country/de"
