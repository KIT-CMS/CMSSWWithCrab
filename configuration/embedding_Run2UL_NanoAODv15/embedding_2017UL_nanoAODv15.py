# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: RECO --step NANO:@TauEmbedding --scenario pp --data --era Run2_2017,run2_nanoAOD_106Xv2 --conditions 150X_dataRun2_v1 --datatier NANOAODSIM --eventcontent NANOAOD --nThreads 2 --number 10 --filein file:MuTauEmbedding-UL2017C_MiniAODv2.root --fileout file:ReReco-MuTauEmbedding-UL2017_NanoAODv15.root --python_filename ReReco-Run2017C-TauEmbedding-UL2017_NanoAODv15_cfg.py --no_exec --customise_commands process.unpackedPatTrigger.triggerResults = cms.InputTag("TriggerResults::SIMembeddingHLT");\
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv2_cff import run2_nanoAOD_106Xv2

process = cms.Process("NANO", Run2_2017, run2_nanoAOD_106Xv2)

# import of standard configurations
process.load("Configuration.StandardSequences.Services_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("PhysicsTools.NanoAOD.nano_cff")
process.load("PhysicsTools.NanoAOD.nano_cff")
process.load("Configuration.StandardSequences.EndOfProcess_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(10),
    output=cms.optional.untracked.allowed(cms.int32, cms.PSet),
)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        "root://cmsdcache-kit-disk.gridka.de//store/group/rucio/pog_tau_group/ul_embedding/large_miniAOD_v2/MuTauFinalState/EmbeddingRun2017B/MINIAOD/inputDoubleMu_106X_ULegacy_miniAOD-v1/0000/032e643e-22b4-447c-b4ae-caa08f9c9a2d.root"
    ),
    secondaryFileNames=cms.untracked.vstring(),
)

process.options = cms.untracked.PSet(
    IgnoreCompletely=cms.untracked.vstring(),
    Rethrow=cms.untracked.vstring(),
    TryToContinue=cms.untracked.vstring(),
    accelerators=cms.untracked.vstring("*"),
    allowUnscheduled=cms.obsolete.untracked.bool,
    canDeleteEarly=cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules=cms.untracked.bool(True),
    dumpOptions=cms.untracked.bool(False),
    emptyRunLumiMode=cms.obsolete.untracked.string,
    eventSetup=cms.untracked.PSet(
        forceNumberOfConcurrentIOVs=cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs=cms.untracked.uint32(0),
    ),
    fileMode=cms.untracked.string("FULLMERGE"),
    forceEventSetupCacheClearOnNewRun=cms.untracked.bool(False),
    holdsReferencesToDeleteEarly=cms.untracked.VPSet(),
    makeTriggerResults=cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue=cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly=cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(0),
    numberOfConcurrentRuns=cms.untracked.uint32(1),
    numberOfStreams=cms.untracked.uint32(0),
    numberOfThreads=cms.untracked.uint32(4),
    printDependencies=cms.untracked.bool(False),
    sizeOfStackForThreadsInKB=cms.optional.untracked.uint32,
    throwIfIllegalParameter=cms.untracked.bool(True),
    wantSummary=cms.untracked.bool(False),
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation=cms.untracked.string("RECO nevts:10"),
    name=cms.untracked.string("Applications"),
    version=cms.untracked.string("$Revision: 1.19 $"),
)

# Output definition

process.NANOAODoutput = cms.OutputModule(
    "NanoAODOutputModule",
    compressionAlgorithm=cms.untracked.string("LZMA"),
    compressionLevel=cms.untracked.int32(9),
    dataset=cms.untracked.PSet(
        dataTier=cms.untracked.string("NANOAODSIM"), filterName=cms.untracked.string("")
    ),
    fileName=cms.untracked.string("file:ReReco-MuTauEmbedding-UL2017_NanoAODv15.root"),
    # fileName = cms.untracked.string('file:/ceph/cwinter/embedding_local/UL2018C_MuTauEmbedding-NanoAODv15/ReReco-MuTauEmbedding-UL2018_NanoAODv15.root'),
    outputCommands=process.NANOAODEventContent.outputCommands,
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "150X_dataRun2_v1", "")


# Path and EndPath definitions
process.nanoAOD_step0 = cms.Path(process.nanoSequence)
process.nanoAOD_step1 = cms.Path(process.nanoSequenceFS)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
process.schedule = cms.Schedule(
    process.nanoAOD_step0,
    process.nanoAOD_step1,
    process.endjob_step,
    process.NANOAODoutput_step,
)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask

associatePatAlgosToolsTask(process)

# Setup FWK for multithreaded
process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeCommon

# call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeCommon(process)

# End of customisation functions

######################## Customisation needed for embedding NanoAOD production ########################
# changes are mainly descibed in the twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauEmbeddingSamplesUL#NanoAOD_Conversion
from PhysicsTools.NanoAOD.common_cff import ExtVar

### create a table with additional embedding information
process.embeddingTable = cms.EDProducer(
    "GlobalVariablesTableProducer",
    name=cms.string("TauEmbedding"),
    variables=cms.PSet(
        nInitialPairCandidates=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "nPairCandidates"),
            float,
            doc="number of muons pairs suitable for selection (for internal studies only)",
        ),
        SelectionOldMass=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "oldMass"),
            float,
            doc="Mass of the Dimuon pair using the old selection algorithm (for internal studies only)",
        ),
        SelectionNewMass=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "newMass"),
            float,
            doc="Mass of the Dimuon pair using the new selection algorithm (for internal studies only)",
        ),
        isMediumLeadingMuon=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "isMediumLeadingMuon"),
            bool,
            doc="leading muon ID (medium)",
        ),
        isMediumTrailingMuon=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "isMediumTrailingMuon"),
            bool,
            doc="trailing muon ID (medium)",
        ),
        isTightLeadingMuon=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "isTightLeadingMuon"),
            bool,
            doc="leading muon ID (tight)",
        ),
        isTightTrailingMuon=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "isTightTrailingMuon"),
            bool,
            doc="trailing muon ID (tight)",
        ),
        initialMETEt=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "initialMETEt"),
            float,
            doc="MET Et of selected event",
        ),
        initialMETphi=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "initialMETphi"),
            float,
            doc="MET phi of selected event",
        ),
        initialPuppiMETEt=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "initialPuppiMETEt"),
            float,
            doc="PuppiMET Et of selected event",
        ),
        initialPuppiMETphi=ExtVar(
            cms.InputTag("selectedMuonsForEmbedding", "initialPuppiMETphi"),
            float,
            doc="PuppiMET phi of selected event",
        ),
    ),
)
process.embeddingTableTask = cms.Task(process.embeddingTable)
process.schedule.associate(process.embeddingTableTask)

### Changes needed to adapt for MiniAODv2 to NanoAODv15 production for embedding:
# There are no lowPtElectrons in the embedding miniAOD, so we need to remove them from the linked objects
process.linkedObjects.lowPtElectrons = ""

process.unpackedPatTrigger.triggerResults = cms.InputTag(
    "TriggerResults::SIMembeddingHLT"
)

process.NANOAODoutput.outputCommands.append(
    "keep edmTriggerResults_*_*_SIMembeddingHLT"
)  # Trigger information
process.NANOAODoutput.outputCommands.append(
    "keep edmTriggerResults_*_*_MERGE"
)  # MET filter flags
process.NANOAODoutput.outputCommands.remove("keep edmTriggerResults_*_*_*")
# process.NANOAODoutput.outputCommands.append("drop *_slimmedLowPtElectrons_*_*")
process.genParticles2HepMC.genEventInfo = cms.InputTag(
    "generator", "", "SIMembeddingpreHLT"
)
process.puppiMetTable.src = cms.InputTag("slimmedMETsPuppi", "", "RERUNPUPPI")
process.rawPuppiMetTable.src = cms.InputTag("slimmedMETsPuppi", "", "RERUNPUPPI")
process.slimmedMETsPuppi.t01Variation = cms.InputTag(
    "slimmedMETsPuppi", "", "RERUNPUPPI"
)
process.metrawCaloPuppi.metSource = cms.InputTag("slimmedMETsPuppi", "", "RERUNPUPPI")
process.source.delayReadingEventProducts = cms.untracked.bool(False)


# Customisation from command line

# Remove Nano table producers related to lowPtElectrons, boosted taus and MC particles which are not present in the embedding miniAOD.
print(
    f"Removal of jetMCTask from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.jetMCTask)}"
)
print(
    f"Removal of metMCTable from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.metMCTable)}"
)
print(
    f"Removal of genProtonTablesTask from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.genProtonTablesTask)}"
)
print(
    f"Removal of ttbarCategoryTableTask from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.ttbarCategoryTableTask)}"
)
print(
    f"Removal of boostedTauMCTask from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.boostedTauMCTask)}"
)
print(
    f"Removal of boostedTauTablesTask from nanoSequence sucessfull: {process.nanoSequence.remove(process.boostedTauTablesTask)}"
)
print(
    f"Removal of lowPtElectronTablesTask from nanoTableTaskCommon sucessfull: {process.nanoTableTaskCommon.remove(process.lowPtElectronTablesTask)}"
)
print(
    f"Removal of lowPtElectronTask from nanoTableTaskCommon sucessfull: {process.nanoTableTaskCommon.remove(process.lowPtElectronTask)}"
)
print(
    f"Removal of lowPtElectronMCTask from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.lowPtElectronMCTask)}"
)
print(
    f"Removal of globalTablesMCTask from nanoSequenceFS sucessfull: {process.nanoSequenceFS.remove(process.globalTablesMCTask)}"
)
print(
    f"Removal of lowPtElectronTask from nanoSequence sucessfull: {process.nanoSequence.remove(process.lowPtElectronTask)}"
)
print(
    f"Removal of lowPtElectronTablesTask from nanoSequence sucessfull: {process.nanoSequence.remove(process.lowPtElectronTablesTask)}"
)

## Add specific trigger filter flags as described in this presentation: https://indico.cern.ch/event/1418386/#23-triggers-in-tau-embedded-sa and in the twiki

# We have to skip the mksel function to avoid the special handling of a "OR" in the string.
# modify the electron entry
process.triggerObjectTable.selections.Electron.qualityBits.extend(
    [
        cms.PSet(
            selection=cms.string("filter('hltEle27WPTightGsfTrackIsoFilter')"),
            doc=cms.string(
                "1e (for e leg trigger object matching in embedding, path HLT_Ele27_WPTight_Gsf)"
            ),
        ),
        cms.PSet(
            selection=cms.string("filter('hltEle32WPTightGsfTrackIsoFilter')"),
            doc=cms.string(
                "1e (for e leg trigger object matching in embedding, path HLT_Ele32_WPTight_Gsf)"
            ),
        ),
        cms.PSet(
            selection=cms.string("filter('hltEle35noerWPTightGsfTrackIsoFilter')"),
            doc=cms.string(
                "1e (for e leg trigger object matching in embedding, path HLT_Ele35_WPTight_Gsf)"
            ),
        ),
        cms.PSet(
            selection=cms.string(
                "filter('hltEle32L1DoubleEGWPTightGsfTrackIsoFilter')"
            ),
            doc=cms.string(
                "1e (for e leg trigger object matching in embedding, path HLT_Ele32_WPTight_L1DoubleEG)"
            ),
        ),
        cms.PSet(
            selection=cms.string("filter('hltEle24erWPTightGsfTrackIsoFilterForTau')"),
            doc=cms.string(
                "e-tau (for e leg trigger object matching in embedding, path HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau*30_eta2p1_CrossL1)"
            ),
        ),
    ]
)

# modify the muon entry
process.triggerObjectTable.selections.Muon.qualityBits.extend(
    [
        cms.PSet(
            selection=cms.string(
                "filter('hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07')"
            ),
            doc=cms.string(
                "1mu (for mu leg trigger object matching in embedding, path HLT_IsoMu24)"
            ),
        ),
        cms.PSet(
            selection=cms.string(
                "filter('hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07')"
            ),
            doc=cms.string(
                "1mu (for mu leg trigger object matching in embedding, path HLT_IsoMu27)"
            ),
        ),
        cms.PSet(
            selection=cms.string(
                "filter('hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07')"
            ),
            doc=cms.string(
                "mu-tau (for mu leg trigger object matching in embedding, path HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 2017)"
            ),
        ),
        cms.PSet(
            selection=cms.string(
                "filter('hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07')"
            ),
            doc=cms.string(
                "mu-tau (for mu leg trigger object matching in embedding, path HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 2018)"
            ),
        ),
    ]
)


# modify the selection string in the tau entry

# change the selection string for tau trigger objects so that the qualityBits can be created properly.
# Added chagens are marked inline
process.triggerObjectTable.selections.Tau.sel = cms.string(
    "( type(84) || type(-100) ) && "  # added "|| type(-100)" to also include L1 Trigger Taus which can be needed by some intermediate filter steps (see https://github.com/cms-sw/cmssw/blob/e3384d3fdf08e8b278c594521574cd6cdea6e9a5/DataFormats/HLTReco/interface/TriggerTypeDefs.h)
    "pt > 5 && "
    "coll('*Tau*') && "
    "( filter('*LooseChargedIso*') || "
    "filter('*MediumChargedIso*') || "
    "filter('*DeepTau*') || "
    "filter('*TightChargedIso*') || "
    "filter('*TightOOSCPhotons*') || "
    "filter('hltL2TauIsoFilter') || "
    "filter('*OverlapFilterIsoMu*') || "
    "filter('*OverlapFilterIsoEle*') || "
    "filter('*L1HLTMatched*') || "
    "filter('*Dz02*') || "
    "filter('*DoublePFTau*') || "
    "filter('*SinglePFTau*') || "
    "filter('hlt*SelectedPFTau') || "
    "filter('*DisplPFTau*') || "
    "filter('*Tau*') )"  # added "|| filter('*Tau*')"
)

process.triggerObjectTable.selections.Tau.qualityBits.extend(
    [
        cms.PSet(
            selection=cms.string(
                "filter('hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3')"
            ),
            doc=cms.string(
                "e-tau (for tau leg trigger object matching in embedding, path HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1)"
            ),
        ),
        cms.PSet(
            selection=cms.string("filter('hltL1sMu18erTau24erIorMu20erTau24er')"),
            doc=cms.string(
                "mu-tau (for tau leg trigger object matching in embedding, path HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 2017)"
            ),
        ),
        cms.PSet(
            selection=cms.string("filter('hltL1sBigORMu18erTauXXer2p1')"),
            doc=cms.string(
                "mu-tau (for tau leg trigger object matching in embedding, path HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 2018)"
            ),
        ),
        cms.PSet(
            selection=cms.string("filter('hltDoubleL2IsoTau26eta2p2')"),
            doc=cms.string(
                "di-tau (for tau leg trigger object matching in embedding, paths HLT_Double*ChargedIsoPFTau*_Trk1*_eta2p1_Reg)"
            ),
        ),
    ]
)


# End of customisation functions


# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete

process = customiseEarlyDelete(process)
# End adding early deletion
