# CMSDAS-tools
Repository for auxiliary tools used in CMSDAS PPS-related exercises

## CMSSW setup
```
cmsrel CMSSW_12_3_0_pre1
cd CMSSW_12_3_0_pre1/src
cmsenv

git cms-init

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j

#setup PPS Direct simulation
git cms-merge-topic orthommel:pps-direct_simu_stdseq-12_3_X
scram b -j

#This package
git clone https://github.com/michael-pitt/CMSDAS-tools.git
scram b -j
```

## Analysis


Analysis code is in [DiLep_analysis.py](https://github.com/michael-pitt/CMSDAS-tools/blob/main/python/DiLep_analysis.py), which select events, compute high level variables and write a skimmed output tree

Two analysis modules can be executed:
- `analysis_mu`: 2 tight muons with opposite charge, mu_pt>50GeV, Electron veto. 
- `analysis_el`: 2 MVAFall17V2IsoWP80 electrons with opposite charge, el_pt>50GeV, Muon veto.
- `analysis_emu`: 1 tightID/ISO muon, 1 MVAFall17V2IsoWP80 electron, lep_pt>20GeV, and opposite charge.

For each event selection:
- An appropriate `keep_and_drop` files can be chosen (see list of files [here](https://github.com/michael-pitt/CMSDAS-tools/tree/main/scripts))
- A corresponding trigger should be set

json file with: [combined_RPIN_CMS_LOWMU.json](https://github.com/michael-pitt/CMSDAS-tools/blob/main/data/combined_RPIN_CMS.json)

### Running on a single file:

example of running on a file from `SingleMuon` stream
```
$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output root://cms-xrd-global.cern.ch//store/data/Run2017H/SingleMuon/NANOAOD/UL2017_MiniAODv2_NanoAODv9-v1/100000/00E28CF6-5CDE-A644-A390-40F2F6613888.root \
--json data/combined_RPIN_CMS_LOWMU.json \
--bi scripts/keep_Data.txt --bo scripts/keep_and_drop_Data_out.txt \
-c "HLT_HIMu15" -I PPSTools.LowPU2017H.LowPU_analysis analysis_mu
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

## Simulation of signal and background

In [LowPU2017H/data/cards](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/data/cards) pythia fragments of the inclusive and diffractive event can be found. 

### MINIAOD

Generation of the MINIAOD using pythia fragments can be done using the [gen_miniaod.sh](https://github.com/michael-pitt/PPSTools/blob/main/LowPU2017H/scripts/gen_miniaod.sh) script.
```
gen_miniaod.sh $card $seed
```
Example:
```
voms-proxy-init --voms cms
scripts/gen_miniaod.sh data/cards/dijet_Pt100_TuneCP5_13TeV 0
```
### NANOAOD
To produce NANOAODs the following sequence should be executed: MINIAOD->MINIAOD+Protons->NANOAOD:

   1. Proton simulation: the code will propagate all final state protons within the RP acceptance, simulate PPS hits, and run the proton reconstruction module.
```
cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/addProtons_miniaod.py inputFiles=file:miniAOD.root instance=""
```
NOTE: Check the input file which collection is used to store the pileup protons.
   2. MINIAOD->NANOAOD step
To produce nanoAOD from miniAOD run:
```
cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/produceNANO.py inputFiles=file:miniAOD_withProtons.root instance=""
```
### Submitting to condor
To produce all steps in one shot, you can run the following script:
```
python scripts/submitMC.py -c data/cards/DYtoLL_Pt12_TuneCP5_13TeV
```
   - add `-s` if you wish to submit the code to condor.
   - add `-j` to set the number of jobs.
   - add `-n` to set the number of events per job.
   


