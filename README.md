# DelayedPhoton 

Plots and limits for delayed photon analysis


setup
-----------------------------
```
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src
mkdir -p HiggsAnalysis
cd HiggsAnalysis
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git CombinedLimit
cd CombinedLimit
git fetch origin
git checkout 81x-root606
scramv1 b clean; scramv1 b
cd ../
git clone git@github.com:cms-lpc-llp/DelayedPhotonLimit.git
cd DelayedPhotonLimit
git checkout Limit2018DNN-D
make
```

If it failed, possibly you need to run singularity first:
```
export SINGULARITY_CACHEDIR=/tmp/qnguyen/singularity;singularity shell -B /cvmfs -B /storage /cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel6
```
to at least after the `scramv1` step to compile the Higgs CombinedLimit tool. After that you can run `make` in normal CMSSW environment without singularity.

Run the analysis step by step

-----------------------------
1. skim the ntuples (not necessary, just to speed up next steps)
-----------------------------
```
cd python
python skim_noBDT.py
```

`skim_noBDT.py` uses variables from `config_noBDT.py`. In particular you need to paste the input list file to `fileNameSigSkim` variable. The list was created by this command:
```
    find ~/DelayedPhoton/CMSSW_10_6_12/src/DelayedPhotonID/deployment/output_bothpho_2017_new_signal -name '*.root'
```

-----------------------------
2. run the fit and obtain datacards
-----------------------------
```
./FitABCD \
/storage/af/user/qnguyen/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2018D/skim_DNN/EGamma_Run2018D.root \
/storage/af/user/qnguyen/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2018D/skim_DNN/GMSB_L100TeV_Ctau10cm_13TeV-pythia8.root \
"L100TeV_Ctau1cm" \
"signal (L100-Ctau10)" \
3J \
datacard \
no \
```

or simply run `source test.sh`.

This will generate the datacard for that signal points
for signals of ctau = 10cm, we use v20 (Closure systematics 90%), for other signal points, we use v18 (Closure systematics 2%)

Regarding `app/FitABCD.cc`:
- The only fitMode that matters is `datacard`. Other mode like `binAndDatacard` is used for optimizing the bin, which is not really necessary because it was done before. Feel free to rerun if you like.
- The only categories that matters are `3J` (for 2-pho category) and `3J1P` (for 1-pho category). The `2J` category was legacy from previous analyses, which requires at least 2 jets instead of 3.
- `useBDT` is always False. We don't use it (legacy from previous analyses). As the result, the output directories are `datacards_3J_noBDT` and  `datacards_3J1P_noBDT` that you should look at.
- Set `_useToy` to `true` for blind analysis. When the data is unblinded, set it to `false`.

After modifying `FitABCD.cc`, remember to `make` again before running the fit with `source test.sh`. 

Once you're sure the code is good, submit it to condor:
```
cd scripts_condor
python create_list.py # to create the input list of signal, which will produce output mylist2017all.list
python submit_datacard_noBDT_ABCD.py mylist2018all.list 3J datacard
```
or 
```
python submit_datacard_noBDT_ABCD.py mylist2018all.list 3J1P datacard # for 1-photon category
```

After condor is done, run `python after_condor.sh` to unpack the output and save it to `combine` directory (indicated by `appDir` variable. 

-----------------------------
3. draw the limit plots
-----------------------------
Once you run all the signal points and you get the limit trees for all of them, you can plot the 2D exclusion region plot (the one in the paper):

```
    cd combine
    python cmd_combine_cards_2018D.sh # to combine 1-pho and 2-pho category
    python cmd_combine_cards_2018ABC_D.sh # to combine with 2018ABC, if you have it
    source cmd_combine_cards_Run2.sh # to combine with 2016 and 2017
    python draw_limits_run2.py
```

