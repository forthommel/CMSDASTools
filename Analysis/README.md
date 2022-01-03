# Analysis
Production of small ntuples from nanoAODs. These ntuples are used in the measurement of exclusive di-lepton cross-section at CMSDAS

## CMSSW setup
```
cmsrel CMSSW_12_3_0_pre1
cd CMSSW_12_3_0_pre1/src
cmsenv

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
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
python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output root://cms-xrd-global.cern.ch//store/data/Run2017H/SingleMuon/NANOAOD/UL2017_MiniAODv2_NanoAODv9-v1/100000/00E28CF6-5CDE-A644-A390-40F2F6613888.root \
--json data/combined_RPIN_CMS_LOWMU.json \
--bi scripts/keep_in.txt --bo scripts/keep_out.txt \
-c "HLT_HIMu15" -I CMSDASTools.Analysis.DiLep_analysis analysis_mudata
```

example of running on a MC (`nano.root` can be replaced by any NANOAOD file)
```
python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output nano.root \
--bi scripts/keep_in.txt --bo scripts/keep_out.txt \
-c "HLT_HIMu15" -I CMSDASTools.Analysis.DiLep_analysis analysis_mumc
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



