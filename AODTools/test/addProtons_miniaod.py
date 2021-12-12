import FWCore.ParameterSet.Config as cms
'''
An example file taken from:
https://github.com/forthommel/cmssw/blob/47b387a9ce910fc84b75c08c059f789a48675db3/SimPPS/Configuration/test/test_miniAOD_cfg.py
'''
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register('era', 'era2017',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "choose era"
                 )			 
options.register('doPUProtons', True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Include PU protons"
                 )
options.register('instance', 'genPUProtons',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "productInstanceName for PU protons"
                 )		                 
options.register('outFilename', 'miniAOD_withProtons.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Output file name"
                 )                 
options.parseArguments()

print("INFO: Era set to", options.era)


#start process
from Configuration.StandardSequences.Eras import eras
from Configuration.ProcessModifiers.run2_miniAOD_UL_cff import run2_miniAOD_UL

if '2016preVFP' in options.era:
    process = cms.Process('PPS',eras.Run2_2016_HIPM,run2_miniAOD_UL)
elif '2016' in options.era:
    process = cms.Process('PPS',eras.Run2_2016,run2_miniAOD_UL)
elif '2017' in options.era:
    process = cms.Process('PPS',eras.Run2_2017,run2_miniAOD_UL)
elif '2018' in options.era:
    process = cms.Process('PPS',eras.Run2_2018,run2_miniAOD_UL)

 
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

#message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    beamDivergenceVtxGenerator = cms.PSet(initialSeed = cms.untracked.uint32(3849)),
    ppsDirectProtonSimulation = cms.PSet(initialSeed = cms.untracked.uint32(4981))
)

# Input source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 
                            )
                            
# Output definition
process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('miniAOD_withProtons.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands
)
# Additional output definition

# Other statements
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
if '2016preVFP' in options.era:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_preVFP_v11', '')
elif '2016' in options.era:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v17', '')
elif '2017' in options.era:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v9', '')
elif '2018' in options.era:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')


# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

outputSteps = [process.endjob_step, process.MINIAODSIMoutput_step]

#schedule execution
toSchedule=[]

#setup proton simulation and reconstruction chains with standard settings:
print('INFO: Run proton simulation for %s configuration '%options.era)
process.load('RecoPPS.Configuration.recoCTPPS_cff')
process.load('SimPPS.Configuration.directSimPPS_cff')
from SimPPS.DirectSimProducer.profile_base_cff import matchDirectSimOutputs
matchDirectSimOutputs(process, miniAOD=True)

process.beamDivergenceVtxGenerator.srcGenParticle = cms.VInputTag(
   #cms.InputTag("genPUProtons","genPUProtons"), # works with step2_premix modifier
   cms.InputTag("genPUProtons",options.instance),
   #cms.InputTag("prunedGenParticles"), # when ~premix_stage2 signal protons proporate to genPUProtons
)

'''
# do not apply vertex smearing again
process.ctppsBeamParametersESSource.vtxStddevX = 0
process.ctppsBeamParametersESSource.vtxStddevY = 0
process.ctppsBeamParametersESSource.vtxStddevZ = 0
  
#undo CMS vertex shift (example)
process.ctppsBeamParametersESSource.vtxOffsetX45 = +0.2475 * 1E-1
process.ctppsBeamParametersESSource.vtxOffsetY45 = -0.6924 * 1E-1
process.ctppsBeamParametersESSource.vtxOffsetZ45 = -8.1100 * 1E-1
'''
  
# for multiRP fit, set if you want to use x* and y* as free parameters or set them to zero
process.ctppsProtons.fitVtxY = True
#if false then ndof=1 and chi2 values will be big (filteredProton container will be empty)

process.pps_fastsim = cms.Path(process.directSimPPS
    * process.recoDirectSimPPS
)

toSchedule.append(process.pps_fastsim)
                           
process.schedule=cms.Schedule( (p for p in toSchedule + outputSteps) )
print(process.schedule)
