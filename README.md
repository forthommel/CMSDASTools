# CMSDAS-tools
Repository for auxiliary tools used in CMSDAS PPS-related exercises

## CMSSW setup
```
cmsrel CMSSW_12_3_0_pre1
cd CMSSW_12_3_0_pre1/src
cmsenv

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j

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

## Analysis


Analysis code is in [DiLep_analysis.py](https://github.com/michael-pitt/CMSDASTools/blob/main/Analysis/python/DiLep_analysis.py), which select events, compute high level variables and write a skimmed output tree

Two analysis modules can be executed:
- `analysis_mu`: 2 tight muons with opposite charge, mu_pt>50GeV, Electron veto. 
- `analysis_el`: 2 MVAFall17V2IsoWP80 electrons with opposite charge, el_pt>50GeV, Muon veto.
- `analysis_emu`: 1 tightID/ISO muon, 1 MVAFall17V2IsoWP80 electron, lep_pt>20GeV, and opposite charge.

For each event selection:
- An appropriate `keep_and_drop` files can be chosen (see list of files [here](https://github.com/michael-pitt/CMSDASTools/tree/main/Analysis/scripts))
- A corresponding trigger should be set

json file with: [combined_RPIN_CMS_LOWMU.json](https://github.com/michael-pitt/CMSDAS-tools/blob/main/data/combined_RPIN_CMS.json)

### Running on a single file:

example of running on a file from `SingleMuon` stream
```
$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output root://cms-xrd-global.cern.ch//store/data/Run2017H/SingleMuon/NANOAOD/UL2017_MiniAODv2_NanoAODv9-v1/100000/00E28CF6-5CDE-A644-A390-40F2F6613888.root \
--json data/combined_RPIN_CMS_LOWMU.json \
--bi scripts/keep_in.txt --bo scripts/keep_out.txt \
-c "HLT_HIMu15" -I CMSDASTools.Analysis.DiLep_analysis analysis_mu
```

### Submitting to condor

To submit condor jobs for an entire data set.
Start a local proxy under the data directory:

```
voms-proxy-init --voms cms --valid 172:00 --out data/voms_proxy.txt
```

Then call:

```
python scripts/processDataset.py  -i /SingleMuon/Run2017H-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD -o /eos/user/p/psilva/data/sdanalysis/SingleMuon/Chunks
```

## Making NANOAOD (with proton info)

The current version of NanoAOD MC samples doesn't include simulated protons. Recently a proton simulation module has been developed, and it is being tested. We will use this new module to add protons to the MC simulation sample and produce nanoAOD with corresponding proton content.

To produce NANOAODs the following sequence should be executed: MINIAOD->MINIAOD+Protons->NANOAOD:

   1. Proton simulation: the code will propagate all final state protons within the RP acceptance, simulate PPS hits, and run the proton reconstruction module.
```
cmsRun $CMSSW_BASE/src/CMSDASTools/AODTools/test/addProtons_miniaod.py inputFiles=file:miniAOD.root instance=""
```
NOTE: Check the input file which collection is used to store the pileup protons.
   2. MINIAOD->NANOAOD step
To produce nanoAOD from miniAOD run:
```
cmsRun $CMSSW_BASE/src/CMSDASTools/AODTools/test/produceNANO.py inputFiles=file:miniAOD_withProtons.root
```
### Submitting to condor
To produce all steps in one shot, you can run the following script:
```
python $CMSSW_BASE/src/CMSDASTools/AODTools/scripts/produceNANOfromDS.py -d /GGToMuMu_Pt-25_Elastic_13TeV-lpair/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
```
   - add `-s` if you wish to submit the code to condor.
   - add `-o` to set the output folder (EOS)
   - add `-n` to set the number of events per job.
   


