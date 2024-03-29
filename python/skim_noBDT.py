from ROOT import *
import os, sys
#sys.path.insert(0, '../')
from config_noBDT import *

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
#################plot settings###########################
axisTitleSize = 0.06
axisTitleOffset = .8
axisTitleSizeRatioX   = 0.18
axisLabelSizeRatioX   = 0.12
axisTitleOffsetRatioX = 0.94
axisTitleSizeRatioY   = 0.15
axisLabelSizeRatioY   = 0.108
axisTitleOffsetRatioY = 0.32

leftMargin   = 0.12
rightMargin  = 0.05
topMargin    = 0.07
bottomMargin = 0.12
##############load delayed photon input tree#############

def GetKeyNames( self, dir = "" ):
    self.cd(dir)
    return [key.GetName() for key in gDirectory.GetListOfKeys()]
def GetClassNames( self, dir = "" ):
    self.cd(dir)
    return [key.GetClassName() for key in gDirectory.GetListOfKeys()]

TFile.GetKeyNames = GetKeyNames
TFile.GetClassNames = GetClassNames


#fileName_all = fileNameSigSkim + fileNameQCDSkim + fileNameGJetsSkim + fileNameDataSkim
#fileName_all = fileNameSigSkim + fileNameQCDSkim + fileNameGJetsSkim + fileNameEWKSkim
#fileName_all = fileNameEWKSkim
#fileName_all = fileNameSigSkim  + fileNameDataSkim + fileNameQCDSkim + fileNameGJetsSkim + fileNameEWKSkim
#fileName_all = fileNameSigSkim # + fileNameDataSkim  
fileName_all = [
'/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/GMSB_L-100TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root',  
'/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/GMSB_L-100TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root',  
'/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/GMSB_L-250TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root',  
'/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/GMSB_L-250TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root',  
'/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/GMSB_L-250TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root',  
]

print "Files to be skimmed:"
print fileName_all

for i in range(0,len(fileName_all)):
    print("=== Skimming file: "+fileName_all[i])

    fileThis = TFile(fileName_all[i], "READ")
    keyList = fileThis.GetKeyNames()
    classList = fileThis.GetClassNames()
    outputFile = TFile(fileName_all[i].replace("/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit","~/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2018D/skim_DNN").replace('L-','L').replace('Ctau-','Ctau').replace('_TuneCP5','').replace('DelayedPhoton_',''),"RECREATE")
    print("Output file: {}".format(outputFile))
    #outputFile = TFile(fileName_all[i].replace("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2018_pho_corr/hadd","/storage/af/user/yeseo/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2018/skim_noBDT").replace('L-','L').replace('Ctau-','Ctau').replace('_TuneCP5',''),"RECREATE")
    outputFile.cd()

    for j in range(0, len(keyList)):
        print classList[j] + "   ===   " + keyList[j]
        if classList[j] == "TTree":
            fileThis.cd()
            inputTree = fileThis.Get(keyList[j])
            print("Input events: {}".format(inputTree.GetEntries()))
            outputFile.cd()
            outputTree = inputTree.CopyTree(cut_skim)
            print("Output events: {}".format(outputTree.GetEntries()))
            outputTree.Write()
        if classList[j] == "TH1F":
            fileThis.cd()
            histThis = fileThis.Get(keyList[j])
            outputFile.cd()
            histThis_out = histThis.Clone()
            histThis_out.Write()

