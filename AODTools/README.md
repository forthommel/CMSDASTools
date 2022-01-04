# CMSDAS-tools
Repository for auxiliary tools used to work with NanoAOD files

## CMSSW setup
```
cmsrel CMSSW_12_3_0_pre1
cd CMSSW_12_3_0_pre1/src
cmsenv

#add nanoAOD package to include protonReco in MC
git cms-addpkg PhysicsTools/NanoAOD
sed -i "s/nanoSequenceOnlyFullSim = .*/nanoSequenceOnlyFullSim = cms.Sequence(cms.Task(protonTablesTask,triggerObjectTablesTask))\n/g" $CMSSW_BASE/src/PhysicsTools/NanoAOD/python/nano_cff.py
scram b -j

#PPS Direct simulation (not in release yet)
git cms-merge-topic forthommel:pps-direct_simu_stdseq-12_3_X
scram b -j

#GenProton info (not in release yet)
git cms-merge-topic forthommel:pps-nanoaod_gen_proton_table-12_2_X
scram b -j


#This package
git clone https://github.com/michael-pitt/CMSDASTools.git
scram b -j
```

## Making NANOAOD (with proton info)

The current version of NanoAOD MC samples doesn't include simulated protons. Recently a proton simulation module has been developed, and it is being tested. We will use this new module to add protons to the MC simulation sample and produce nanoAOD with corresponding proton content.

To produce NANOAODs the following sequence should be executed: MINIAOD->MINIAOD+Protons->NANOAOD:

   1. Proton simulation: the code will propagate all final state protons within the RP acceptance, simulate PPS hits, and run the proton reconstruction module.
```
cmsRun $CMSSW_BASE/src/CMSDASTools/AODTools/test/addProtons_miniaod.py inputFiles=file:miniAOD.root era="era2018" instance=""
```
NOTE: Check the input file which collection is used to store the pileup protons.
   2. MINIAOD->NANOAOD step
To produce nanoAOD from miniAOD run:
```
cmsRun $CMSSW_BASE/src/CMSDASTools/AODTools/test/produceNANO.py inputFiles=file:miniAOD_withProtons.root era="era2018" outFilename=output_nano.root
```

### Submitting to condor
To produce all steps in one shot, you can run the following script:
```
python scripts/produceNANOfromDS.py -d /GGToMuMu_Pt-25_Elastic_13TeV-lpair/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
```
   - add `-s` if you wish to submit the code to condor.
   - add `-o` to set the output folder (EOS)
   - add `-n` to set the number of events per job.
   

