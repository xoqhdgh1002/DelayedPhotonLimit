#!/bin/bash

./FitABCD \
./2018D/skim_DNN/EGamma_Run2018D.root \
./2018D/skim_DNN/GMSB_L100TeV_Ctau10cm_13TeV-pythia8.root \
"L100TeV_Ctau10cm" \
"signal (L100-Ctau10)" \
3J1P \
datacard \
no

echo "Datacard created"
cd fit_results/2018D/datacards_3J1P_noBDT 
combine DelayedPhotonCard_L100TeV_Ctau10cm.txt -M Asymptotic -n L100TeV_Ctau10cm_2018CAT1
