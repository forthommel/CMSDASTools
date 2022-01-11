# Analysis
Production of small ntuples from nanoAODs. These ntuples are used in the measurement of exclusive di-lepton cross-section at CMSDAS

## CMSSW setup
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
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

For each event selection:
- An appropriate `keep_and_drop` files can be chosen (see list of files [here](https://github.com/michael-pitt/CMSDASTools/tree/main/Analysis/scripts))
- A corresponding trigger should be set

json file are stored in [data](https://github.com/michael-pitt/CMSDASTools/tree/main/data) folder

### Running on a single file:

example of running on a file from `SingleMuon` stream
```
python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/C218937D-A2AC-9949-8E65-D14C50F824AF.root \
--json ${CMSSW_BASE}/src/CMSDASTools/Analysis/data/CMSgolden_2RPGood_anyarms.json \
--bi $CMSSW_BASE/src/CMSDASTools/Analysis/scripts/keep_in.txt \
--bo $CMSSW_BASE/src/CMSDASTools/Analysis/scripts/keep_out.txt \
-c "HLT_IsoMu24" -I CMSDASTools.Analysis.DiLep_analysis analysis_mudata
```

example of running on a MC (`nano.root` can be replaced by any NANOAOD file)
```
python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
output nano.root \
--bi $CMSSW_BASE/src/CMSDASTools/Analysis/scripts/keep_in.txt \
--bo $CMSSW_BASE/src/CMSDASTools/Analysis/scripts/keep_out.txt \
-c "1" -I CMSDASTools.Analysis.DiLep_analysis analysis_mumc
```

### Submitting to condor

To submit condor jobs for an entire data set:

You can use [runNtuplizer.py](https://github.com/michael-pitt/CMSDASTools/blob/main/Analysis/scripts/runNtuplizer.py) script to submit jobs from a list of datasets.
The list of datasets should be provided as a `txt` file, for example [listSamples.txt](https://github.com/michael-pitt/CMSDASTools/blob/main/Analysis/data/listSamples.txt).

Run the following command
```
python $CMSSW_BASE/src/CMSDASTools/Analysis/scripts/runNtuplizer.py --in $CMSSW_BASE/src/CMSDASTools/Analysis/data/listSamples.txt
```
with options
- `--out`: Output folder (for example */eos/home-X/$USER/...*)
- `--in`: Input *txt* file with list of datasets or folders where NANOAOD are stored

NOTE: When executing the script, you will be requested to create a `proxy` in the submission foder:

```
voms-proxy-init --voms cms --valid 72:00 --out $PWD/FarmLocalNtuple/myproxy509
```

### Merging results

To merge the output files, run [haddnano.py](https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/scripts/haddnano.py) script:
```
python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py output.root ListOfROOTFiles
```
