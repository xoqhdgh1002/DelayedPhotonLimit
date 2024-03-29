from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import weight_cut
from Aux import getXsecBR

fileNameData = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root'
fileNameSig1 = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root'
fileNameSig2 = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root'
fileNameSig3 = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau1200cm_13TeV-pythia8.root'

xsec_Sig1, exsec_Sig1 =  getXsecBR(200,10)
xsec_Sig2, exsec_Sig2 =  getXsecBR(200,200)
xsec_Sig3, exsec_Sig3 =  getXsecBR(200,1200)

gROOT.SetBatch(True)

cut_blind = "(pho1ClusterTime_SmearToData < 1 || t1MET < 300)"
cut_preSelection = " 1>0 "
cut_trigger = "(HLTDecision[81] == 1)"
cut_nPhotons = " n_Photons == 2 && pho2SigmaIetaIeta<0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso<30.0 && pho2sumNeutralHadronEt<30.0 && pho2trkSumPtHollowConeDR03 < 30.0"
cut_photonID_Pt = "pho1Pt > 70"
pho1passSigmaIetaIetaTight = "pho1passSigmaIetaIetaTight"
pho1passHoverETight = "&& pho1passHoverETight"
cut_photonID_Eta = "pho1Pt > 70 && abs(pho1Eta)<1.4442"
cut_photonID_Iso = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso"
cut_photonID_EleVeto = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto"
cut_photonID_Smajor = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight"
cut_photonID_Sminor = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight && pho1Sminor<0.4"
cut_photonID_R9 = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight && pho1Sminor<0.4 && pho1R9 > 0.9"
cut_photonID_SigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight && pho1Sminor<0.4 && pho1R9 > 0.9&& "+pho1passSigmaIetaIetaTight
cut_photonID_HoverE = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight && pho1Sminor<0.4 && pho1R9 > 0.9 && "+pho1passSigmaIetaIetaTight+pho1passHoverETight
cut_photonID = "pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight && pho1Sminor<0.4 && pho1R9 > 0.9&& "+pho1passSigmaIetaIetaTight+pho1passHoverETight
cut_nJets = "n_Jets > 2"
cut_lepVeto = "nTightMuons == 0"
cut_MET_filter = "Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"


print "final cut ===> "+weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&" + cut_lepVeto + "&&"+cut_nPhotons+"&&"+cut_MET_filter+")"


inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

tableFileName = "./cut_flow_Table.txt"
#Data
fileData = TFile(fileNameData)
treeData = fileData.Get("DelayedPhoton")
n_blindData = 84703010.0 #treeData.GetEntries(cut_blind)
print n_blindData
n_photonID_PtData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_Pt)
n_photonID_EtaData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_Eta)
n_photonID_IsoData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_Iso)
n_photonID_EleVetoData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_EleVeto)
n_photonID_SmajorData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_Smajor)
n_photonID_SminorData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_Sminor)
n_photonID_R9Data = treeData.GetEntries(cut_blind+"&&"+cut_photonID_R9)
n_photonID_SigmaIetaIetaData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_SigmaIetaIeta)
n_photonID_HoverEData = treeData.GetEntries(cut_blind+"&&"+cut_photonID_HoverE)

n_photonIDData = treeData.GetEntries(cut_blind+"&&"+cut_photonID)
print n_photonIDData

n_nJetsData = treeData.GetEntries(cut_blind+"&&"+cut_photonID+"&&"+cut_nJets)
print n_nJetsData
n_lepVetoData = treeData.GetEntries(cut_blind+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto)
print n_lepVetoData
n_nPhotonsData = treeData.GetEntries(cut_blind+"&&"+cut_photonID+"&&"+cut_nJets+"&&" + cut_lepVeto +"&&"+cut_nPhotons)
print n_nPhotonsData
n_MET_filterData = treeData.GetEntries(cut_blind+"&&"+cut_photonID+"&&"+cut_nJets+"&&" + cut_lepVeto +"&&"+cut_nPhotons+"&&"+cut_MET_filter)
print n_MET_filterData

n_triggerData = treeData.GetEntries(cut_blind+"&&"+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&" + cut_lepVeto +"&&"+cut_nPhotons+"&&"+cut_MET_filter)
print n_triggerData

#Sig1
fileSig1 = TFile(fileNameSig1)
hNEventsThis_Sig1 = fileSig1.Get("NEvents")
N_total_Sig1 = hNEventsThis_Sig1.GetBinContent(1)
lumi_xs_Sig1 = xsec_Sig1*35922.0/N_total_Sig1
N_beforePreselection_Sig1 =  lumi_xs_Sig1*N_total_Sig1
treeSig1 = fileSig1.Get("DelayedPhoton")
hist_blindSig1 = TH1F("hist_blindSig1","hist_blindSig1",100,0,100)
hist_triggerSig1 = TH1F("hist_triggerSig1","hist_triggerSig1",100,0,100)
hist_photonID_PtSig1 = TH1F("hist_photonID_PtSig1","hist_photonID_PtSig1",100,0,100)
hist_photonID_EtaSig1 = TH1F("hist_photonID_EtaSig1","hist_photonID_EtaSig1",100,0,100)
hist_photonID_IsoSig1 = TH1F("hist_photonID_IsoSig1","hist_photonID_IsoSig1",100,0,100)
hist_photonID_EleVetoSig1 = TH1F("hist_photonID_EleVetoSig1","hist_photonID_EleVetoSig1",100,0,100)
hist_photonID_SmajorSig1 = TH1F("hist_photonID_SmajorSig1","hist_photonID_SmajorSig1",100,0,100)
hist_photonID_SminorSig1 = TH1F("hist_photonID_SminorSig1","hist_photonID_SminorSig1",100,0,100)
hist_photonID_R9Sig1 = TH1F("hist_photonID_R9Sig1","hist_photonID_R9Sig1",100,0,100)
hist_photonID_SigmaIetaIetaSig1 = TH1F("hist_photonID_SigmaIetaIetaSig1","hist_photonID_SigmaIetaIetaSig1",100,0,100)
hist_photonID_HoverESig1 = TH1F("hist_photonID_HoverESig1","hist_photonID_HoverESig1",100,0,100)
hist_photonIDSig1 = TH1F("hist_photonIDSig1","hist_photonIDSig1",100,0,100)
hist_nJetsSig1 = TH1F("hist_nJetsSig1","hist_nJetsSig1",100,0,100)
hist_lepVetoSig1 = TH1F("hist_lepVetoSig1","hist_lepVetoSig1",100,0,100)
hist_nPhotonsSig1 = TH1F("hist_nPhotonsSig1","hist_nPhotonsSig1",100,0,100)
hist_MET_filterSig1 = TH1F("hist_MET_filterSig1","hist_MET_filterSig1",100,0,100)
treeSig1.Draw("NPU>>hist_blindSig1",weight_cut+"("+cut_preSelection+")")
n_blindSig1 = lumi_xs_Sig1*hist_blindSig1.Integral()
print n_blindSig1
treeSig1.Draw("NPU>>hist_photonID_PtSig1",weight_cut+"("+cut_photonID_Pt+")")
treeSig1.Draw("NPU>>hist_photonID_EtaSig1",weight_cut+"("+cut_photonID_Eta+")")
treeSig1.Draw("NPU>>hist_photonID_IsoSig1",weight_cut+"("+cut_photonID_Iso+")")
treeSig1.Draw("NPU>>hist_photonID_SmajorSig1",weight_cut+"("+cut_photonID_Smajor+")")
treeSig1.Draw("NPU>>hist_photonID_SminorSig1",weight_cut+"("+cut_photonID_Sminor+")")
treeSig1.Draw("NPU>>hist_photonID_R9Sig1",weight_cut+"("+cut_photonID_R9+")")
treeSig1.Draw("NPU>>hist_photonID_EleVetoSig1",weight_cut+"("+cut_photonID_EleVeto+")")
treeSig1.Draw("NPU>>hist_photonID_SigmaIetaIetaSig1",weight_cut+"("+cut_photonID_SigmaIetaIeta+")")
treeSig1.Draw("NPU>>hist_photonID_HoverESig1",weight_cut+"("+cut_photonID_HoverE+")")
treeSig1.Draw("NPU>>hist_photonIDSig1",weight_cut+"("+cut_photonID+")")
n_photonID_PtSig1 = lumi_xs_Sig1*hist_photonID_PtSig1.Integral()
n_photonID_EtaSig1 = lumi_xs_Sig1*hist_photonID_EtaSig1.Integral()
n_photonID_IsoSig1 = lumi_xs_Sig1*hist_photonID_IsoSig1.Integral()
n_photonID_EleVetoSig1 = lumi_xs_Sig1*hist_photonID_EleVetoSig1.Integral()
n_photonID_SmajorSig1 = lumi_xs_Sig1*hist_photonID_SmajorSig1.Integral()
n_photonID_SminorSig1 = lumi_xs_Sig1*hist_photonID_SminorSig1.Integral()
n_photonID_R9Sig1 = lumi_xs_Sig1*hist_photonID_R9Sig1.Integral()
n_photonID_SigmaIetaIetaSig1 = lumi_xs_Sig1*hist_photonID_SigmaIetaIetaSig1.Integral()
n_photonID_HoverESig1 = lumi_xs_Sig1*hist_photonID_HoverESig1.Integral()
n_photonIDSig1 = lumi_xs_Sig1*hist_photonIDSig1.Integral()
print n_photonIDSig1
treeSig1.Draw("NPU>>hist_nJetsSig1",weight_cut+"("+cut_photonID+"&&"+cut_nJets+")")
n_nJetsSig1 = lumi_xs_Sig1*hist_nJetsSig1.Integral()
print n_nJetsSig1
treeSig1.Draw("NPU>>hist_lepVetoSig1",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+")")
n_lepVetoSig1 = lumi_xs_Sig1*hist_lepVetoSig1.Integral()
print n_lepVetoSig1
treeSig1.Draw("NPU>>hist_nPhotonsSig1",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+")")
n_nPhotonsSig1 = lumi_xs_Sig1*hist_nPhotonsSig1.Integral()
print n_nPhotonsSig1
treeSig1.Draw("NPU>>hist_MET_filterSig1",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
n_MET_filterSig1 = lumi_xs_Sig1*hist_MET_filterSig1.Integral()
print n_MET_filterSig1
print n_blindSig1/np.sqrt(n_blindSig1)
treeSig1.Draw("NPU>>hist_triggerSig1",weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
n_triggerSig1 = lumi_xs_Sig1*hist_triggerSig1.Integral()
print n_triggerSig1
print int(100.0*n_triggerSig1/n_blindSig1)

#Sig2
fileSig2 = TFile(fileNameSig2)
hNEventsThis_Sig2 = fileSig2.Get("NEvents")
N_total_Sig2 = hNEventsThis_Sig2.GetBinContent(1)
lumi_xs_Sig2 = xsec_Sig2*35922.0/N_total_Sig2
N_beforePreselection_Sig2 =  lumi_xs_Sig2*N_total_Sig2
treeSig2 = fileSig2.Get("DelayedPhoton")
hist_blindSig2 = TH1F("hist_blindSig2","hist_blindSig2",100,0,100)
hist_triggerSig2 = TH1F("hist_triggerSig2","hist_triggerSig2",100,0,100)
hist_photonID_PtSig2 = TH1F("hist_photonID_PtSig2","hist_photonID_PtSig2",100,0,100)
hist_photonID_EtaSig2 = TH1F("hist_photonID_EtaSig2","hist_photonID_EtaSig2",100,0,100)
hist_photonID_IsoSig2 = TH1F("hist_photonID_IsoSig2","hist_photonID_IsoSig2",100,0,100)
hist_photonID_EleVetoSig2 = TH1F("hist_photonID_EleVetoSig2","hist_photonID_EleVetoSig2",100,0,100)
hist_photonID_SmajorSig2 = TH1F("hist_photonID_SmajorSig2","hist_photonID_SmajorSig2",100,0,100)
hist_photonID_SminorSig2 = TH1F("hist_photonID_SminorSig2","hist_photonID_SminorSig2",100,0,100)
hist_photonID_R9Sig2 = TH1F("hist_photonID_R9Sig2","hist_photonID_R9Sig2",100,0,100)
hist_photonID_SigmaIetaIetaSig2 = TH1F("hist_photonID_SigmaIetaIetaSig2","hist_photonID_SigmaIetaIetaSig2",100,0,100)
hist_photonID_HoverESig2 = TH1F("hist_photonID_HoverESig2","hist_photonID_HoverESig2",100,0,100)
hist_photonIDSig2 = TH1F("hist_photonIDSig2","hist_photonIDSig2",100,0,100)
hist_nJetsSig2 = TH1F("hist_nJetsSig2","hist_nJetsSig2",100,0,100)
hist_lepVetoSig2 = TH1F("hist_lepVetoSig2","hist_lepVetoSig2",100,0,100)
hist_nPhotonsSig2 = TH1F("hist_nPhotonsSig2","hist_nPhotonsSig2",100,0,100)
hist_MET_filterSig2 = TH1F("hist_MET_filterSig2","hist_MET_filterSig2",100,0,100)
treeSig2.Draw("NPU>>hist_blindSig2",weight_cut+"("+cut_preSelection+")")
n_blindSig2 = lumi_xs_Sig2*hist_blindSig2.Integral()
print n_blindSig2
treeSig2.Draw("NPU>>hist_photonID_PtSig2",weight_cut+"("+cut_photonID_Pt+")")
treeSig2.Draw("NPU>>hist_photonID_EtaSig2",weight_cut+"("+cut_photonID_Eta+")")
treeSig2.Draw("NPU>>hist_photonID_IsoSig2",weight_cut+"("+cut_photonID_Iso+")")
treeSig2.Draw("NPU>>hist_photonID_SmajorSig2",weight_cut+"("+cut_photonID_Smajor+")")
treeSig2.Draw("NPU>>hist_photonID_SminorSig2",weight_cut+"("+cut_photonID_Sminor+")")
treeSig2.Draw("NPU>>hist_photonID_R9Sig2",weight_cut+"("+cut_photonID_R9+")")
treeSig2.Draw("NPU>>hist_photonID_EleVetoSig2",weight_cut+"("+cut_photonID_EleVeto+")")
treeSig2.Draw("NPU>>hist_photonID_SigmaIetaIetaSig2",weight_cut+"("+cut_photonID_SigmaIetaIeta+")")
treeSig2.Draw("NPU>>hist_photonID_HoverESig2",weight_cut+"("+cut_photonID_HoverE+")")
treeSig2.Draw("NPU>>hist_photonIDSig2",weight_cut+"("+cut_photonID+")")
n_photonID_PtSig2 = lumi_xs_Sig2*hist_photonID_PtSig2.Integral()
n_photonID_EtaSig2 = lumi_xs_Sig2*hist_photonID_EtaSig2.Integral()
n_photonID_IsoSig2 = lumi_xs_Sig2*hist_photonID_IsoSig2.Integral()
n_photonID_EleVetoSig2 = lumi_xs_Sig2*hist_photonID_EleVetoSig2.Integral()
n_photonID_SmajorSig2 = lumi_xs_Sig2*hist_photonID_SmajorSig2.Integral()
n_photonID_SminorSig2 = lumi_xs_Sig2*hist_photonID_SminorSig2.Integral()
n_photonID_R9Sig2 = lumi_xs_Sig2*hist_photonID_R9Sig2.Integral()
n_photonID_SigmaIetaIetaSig2 = lumi_xs_Sig2*hist_photonID_SigmaIetaIetaSig2.Integral()
n_photonID_HoverESig2 = lumi_xs_Sig2*hist_photonID_HoverESig2.Integral()
n_photonIDSig2 = lumi_xs_Sig2*hist_photonIDSig2.Integral()
print n_photonIDSig2
treeSig2.Draw("NPU>>hist_nJetsSig2",weight_cut+"("+cut_photonID+"&&"+cut_nJets+")")
n_nJetsSig2 = lumi_xs_Sig2*hist_nJetsSig2.Integral()
print n_nJetsSig2
treeSig2.Draw("NPU>>hist_lepVetoSig2",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+")")
n_lepVetoSig2 = lumi_xs_Sig2*hist_lepVetoSig2.Integral()
print n_lepVetoSig2
treeSig2.Draw("NPU>>hist_nPhotonsSig2",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+")")
n_nPhotonsSig2 = lumi_xs_Sig2*hist_nPhotonsSig2.Integral()
print n_nPhotonsSig2
treeSig2.Draw("NPU>>hist_MET_filterSig2",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
n_MET_filterSig2 = lumi_xs_Sig2*hist_MET_filterSig2.Integral()
print n_MET_filterSig2
print n_blindSig2/np.sqrt(n_blindSig2)
treeSig2.Draw("NPU>>hist_triggerSig2",weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
n_triggerSig2 = lumi_xs_Sig2*hist_triggerSig2.Integral()
print n_triggerSig2
print int(100.0*n_triggerSig2/n_blindSig2)


#Sig3
fileSig3 = TFile(fileNameSig3)
hNEventsThis_Sig3 = fileSig3.Get("NEvents")
N_total_Sig3 = hNEventsThis_Sig3.GetBinContent(1)
lumi_xs_Sig3 = xsec_Sig3*35922.0/N_total_Sig3
N_beforePreselection_Sig3 =  lumi_xs_Sig3*N_total_Sig3
treeSig3 = fileSig3.Get("DelayedPhoton")
hist_blindSig3 = TH1F("hist_blindSig3","hist_blindSig3",100,0,100)
hist_triggerSig3 = TH1F("hist_triggerSig3","hist_triggerSig3",100,0,100)
hist_photonID_PtSig3 = TH1F("hist_photonID_PtSig3","hist_photonID_PtSig3",100,0,100)
hist_photonID_EtaSig3 = TH1F("hist_photonID_EtaSig3","hist_photonID_EtaSig3",100,0,100)
hist_photonID_IsoSig3 = TH1F("hist_photonID_IsoSig3","hist_photonID_IsoSig3",100,0,100)
hist_photonID_EleVetoSig3 = TH1F("hist_photonID_EleVetoSig3","hist_photonID_EleVetoSig3",100,0,100)
hist_photonID_SmajorSig3 = TH1F("hist_photonID_SmajorSig3","hist_photonID_SmajorSig3",100,0,100)
hist_photonID_SminorSig3 = TH1F("hist_photonID_SminorSig3","hist_photonID_SminorSig3",100,0,100)
hist_photonID_R9Sig3 = TH1F("hist_photonID_R9Sig3","hist_photonID_R9Sig3",100,0,100)
hist_photonID_SigmaIetaIetaSig3 = TH1F("hist_photonID_SigmaIetaIetaSig3","hist_photonID_SigmaIetaIetaSig3",100,0,100)
hist_photonID_HoverESig3 = TH1F("hist_photonID_HoverESig3","hist_photonID_HoverESig3",100,0,100)
hist_photonIDSig3 = TH1F("hist_photonIDSig3","hist_photonIDSig3",100,0,100)
hist_nJetsSig3 = TH1F("hist_nJetsSig3","hist_nJetsSig3",100,0,100)
hist_lepVetoSig3 = TH1F("hist_lepVetoSig3","hist_lepVetoSig3",100,0,100)
hist_nPhotonsSig3 = TH1F("hist_nPhotonsSig3","hist_nPhotonsSig3",100,0,100)
hist_MET_filterSig3 = TH1F("hist_MET_filterSig3","hist_MET_filterSig3",100,0,100)
treeSig3.Draw("NPU>>hist_blindSig3",weight_cut+"("+cut_preSelection+")")
n_blindSig3 = lumi_xs_Sig3*hist_blindSig3.Integral()
print n_blindSig3
treeSig3.Draw("NPU>>hist_photonID_PtSig3",weight_cut+"("+cut_photonID_Pt+")")
treeSig3.Draw("NPU>>hist_photonID_EtaSig3",weight_cut+"("+cut_photonID_Eta+")")
treeSig3.Draw("NPU>>hist_photonID_IsoSig3",weight_cut+"("+cut_photonID_Iso+")")
treeSig3.Draw("NPU>>hist_photonID_SmajorSig3",weight_cut+"("+cut_photonID_Smajor+")")
treeSig3.Draw("NPU>>hist_photonID_SminorSig3",weight_cut+"("+cut_photonID_Sminor+")")
treeSig3.Draw("NPU>>hist_photonID_R9Sig3",weight_cut+"("+cut_photonID_R9+")")
treeSig3.Draw("NPU>>hist_photonID_EleVetoSig3",weight_cut+"("+cut_photonID_EleVeto+")")
treeSig3.Draw("NPU>>hist_photonID_SigmaIetaIetaSig3",weight_cut+"("+cut_photonID_SigmaIetaIeta+")")
treeSig3.Draw("NPU>>hist_photonID_HoverESig3",weight_cut+"("+cut_photonID_HoverE+")")
treeSig3.Draw("NPU>>hist_photonIDSig3",weight_cut+"("+cut_photonID+")")
n_photonID_PtSig3 = lumi_xs_Sig3*hist_photonID_PtSig3.Integral()
n_photonID_EtaSig3 = lumi_xs_Sig3*hist_photonID_EtaSig3.Integral()
n_photonID_IsoSig3 = lumi_xs_Sig3*hist_photonID_IsoSig3.Integral()
n_photonID_EleVetoSig3 = lumi_xs_Sig3*hist_photonID_EleVetoSig3.Integral()
n_photonID_SmajorSig3 = lumi_xs_Sig3*hist_photonID_SmajorSig3.Integral()
n_photonID_SminorSig3 = lumi_xs_Sig3*hist_photonID_SminorSig3.Integral()
n_photonID_R9Sig3 = lumi_xs_Sig3*hist_photonID_R9Sig3.Integral()
n_photonID_SigmaIetaIetaSig3 = lumi_xs_Sig3*hist_photonID_SigmaIetaIetaSig3.Integral()
n_photonID_HoverESig3 = lumi_xs_Sig3*hist_photonID_HoverESig3.Integral()
n_photonIDSig3 = lumi_xs_Sig3*hist_photonIDSig3.Integral()
print n_photonIDSig3
treeSig3.Draw("NPU>>hist_nJetsSig3",weight_cut+"("+cut_photonID+"&&"+cut_nJets+")")
n_nJetsSig3 = lumi_xs_Sig3*hist_nJetsSig3.Integral()
print n_nJetsSig3
treeSig3.Draw("NPU>>hist_lepVetoSig3",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+")")
n_lepVetoSig3 = lumi_xs_Sig3*hist_lepVetoSig3.Integral()
print n_lepVetoSig3
treeSig3.Draw("NPU>>hist_nPhotonsSig3",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+")")
n_nPhotonsSig3 = lumi_xs_Sig3*hist_nPhotonsSig3.Integral()
print n_nPhotonsSig3
treeSig3.Draw("NPU>>hist_MET_filterSig3",weight_cut+"("+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
n_MET_filterSig3 = lumi_xs_Sig3*hist_MET_filterSig3.Integral()
print n_MET_filterSig3
print n_blindSig3/np.sqrt(n_blindSig3)
treeSig3.Draw("NPU>>hist_triggerSig3",weight_cut+"("+cut_trigger+"&&"+cut_photonID+"&&"+cut_nJets+"&&"+cut_lepVeto+"&&"+cut_nPhotons+"&&"+cut_MET_filter+")")
n_triggerSig3 = lumi_xs_Sig3*hist_triggerSig3.Integral()
print n_triggerSig3
print int(100.0*n_triggerSig3/n_blindSig3)



f1=open(tableFileName, 'a')

print >> f1, "\\multirow{2}{*}{cuts} & \\multirow{2}{*}{nEvents in data} & \multicolumn{3}{*}{nEvents in signal} \\\\"
print >> f1, " & & $\\Lambda=200, c\\tau=10$ & $\\Lambda=200, c\\tau=200$ & $\\Lambda=200, c\\tau=1200$ \\\\"
print >> f1,  "without cut & "+ "- & "+"%.2f " % N_beforePreselection_Sig1 + "(100\\%) & "+ "%.2f " % N_beforePreselection_Sig2 + "(100\\%) & "+"%.2f " % N_beforePreselection_Sig3 + "(100\\%)"+ "\\\\"
print >> f1,  "with pre-selection ($p_T>40$, $|\\eta|<1.4442$, eVeto) & "+ "%.0f " % n_blindData + "(100\\%)& "+"%.2f " % n_blindSig1 + "("+"%.1f"%float(100.0*n_blindSig1/N_beforePreselection_Sig1)+"\\%) & "+ "%.2f " % n_blindSig2 + "("+"%.1f"%float(100.0*n_blindSig2/N_beforePreselection_Sig2)+"\\%) & "+ "%.2f " % n_blindSig3 + "("+"%.1f"%float(100.0*n_blindSig3/N_beforePreselection_Sig3)+"\\%) "+ "\\\\"
print >> f1,  "+ photon $p_T$ cut& "+"%.0f" % n_photonID_PtData+"("+"%.1f"%float(100.0*n_photonID_PtData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_PtSig1 + "("+"%.1f"%float(100.0*n_photonID_PtSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_PtSig2 + "("+"%.1f"%float(100.0*n_photonID_PtSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_PtSig3 + "("+"%.1f"%float(100.0*n_photonID_PtSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon Isolation cut& "+"%.0f" % n_photonID_IsoData+"("+"%.1f"%float(100.0*n_photonID_IsoData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_IsoSig1 + "("+"%.1f"%float(100.0*n_photonID_IsoSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_IsoSig2 + "("+"%.1f"%float(100.0*n_photonID_IsoSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_IsoSig3 + "("+"%.1f"%float(100.0*n_photonID_IsoSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon eVeto cut& "+"%.0f" % n_photonID_EleVetoData+"("+"%.1f"%float(100.0*n_photonID_EleVetoData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_EleVetoSig1 + "("+"%.1f"%float(100.0*n_photonID_EleVetoSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_EleVetoSig2 + "("+"%.1f"%float(100.0*n_photonID_EleVetoSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_EleVetoSig3 + "("+"%.1f"%float(100.0*n_photonID_EleVetoSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon $S_{major}$ cut& "+"%.0f" % n_photonID_SmajorData+"("+"%.1f"%float(100.0*n_photonID_SmajorData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_SmajorSig1 + "("+"%.1f"%float(100.0*n_photonID_SmajorSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_SmajorSig2 + "("+"%.1f"%float(100.0*n_photonID_SmajorSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_SmajorSig3 + "("+"%.1f"%float(100.0*n_photonID_SmajorSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon $S_{minor}$ cut& "+"%.0f" % n_photonID_SminorData+"("+"%.1f"%float(100.0*n_photonID_SminorData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_SminorSig1 + "("+"%.1f"%float(100.0*n_photonID_SminorSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_SminorSig2 + "("+"%.1f"%float(100.0*n_photonID_SminorSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_SminorSig3 + "("+"%.1f"%float(100.0*n_photonID_SminorSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon $R_{9}$ cut& "+"%.0f" % n_photonID_R9Data+"("+"%.1f"%float(100.0*n_photonID_R9Data/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_R9Sig1 + "("+"%.1f"%float(100.0*n_photonID_R9Sig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_R9Sig2 + "("+"%.1f"%float(100.0*n_photonID_R9Sig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_R9Sig3 + "("+"%.1f"%float(100.0*n_photonID_R9Sig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon $\\sigma_i\\etai\\eta$ cut& "+"%.0f" % n_photonID_SigmaIetaIetaData+"("+"%.1f"%float(100.0*n_photonID_SigmaIetaIetaData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_SigmaIetaIetaSig1 + "("+"%.1f"%float(100.0*n_photonID_SigmaIetaIetaSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_SigmaIetaIetaSig2 + "("+"%.1f"%float(100.0*n_photonID_SigmaIetaIetaSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_SigmaIetaIetaSig3 + "("+"%.1f"%float(100.0*n_photonID_SigmaIetaIetaSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ photon $H/E$ cut& "+"%.0f" % n_photonID_HoverEData+"("+"%.1f"%float(100.0*n_photonID_HoverEData/n_blindData)+"\\%)  & "+"%.2f"%n_photonID_HoverESig1 + "("+"%.1f"%float(100.0*n_photonID_HoverESig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_photonID_HoverESig2 + "("+"%.1f"%float(100.0*n_photonID_HoverESig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_photonID_HoverESig3 + "("+"%.1f"%float(100.0*n_photonID_HoverESig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ nJets cut& "+"%.0f" % n_nJetsData+"("+"%.1f"%float(100.0*n_nJetsData/n_blindData)+"\\%)  & "+"%.2f"%n_nJetsSig1 + "("+"%.1f"%float(100.0*n_nJetsSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_nJetsSig2 + "("+"%.1f"%float(100.0*n_nJetsSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_nJetsSig3 + "("+"%.1f"%float(100.0*n_nJetsSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ lepton Veto cut& "+"%.0f" % n_lepVetoData+"("+"%.1f"%float(100.0*n_lepVetoData/n_blindData)+"\\%)  & "+"%.2f"%n_lepVetoSig1 + "("+"%.1f"%float(100.0*n_lepVetoSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_lepVetoSig2 + "("+"%.1f"%float(100.0*n_lepVetoSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_lepVetoSig3 + "("+"%.1f"%float(100.0*n_lepVetoSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ nPhotons cut& "+"%.0f" % n_nPhotonsData+"("+"%.1f"%float(100.0*n_nPhotonsData/n_blindData)+"\\%)  & "+"%.2f"%n_nPhotonsSig1 + "("+"%.1f"%float(100.0*n_nPhotonsSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_nPhotonsSig2 + "("+"%.1f"%float(100.0*n_nPhotonsSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_nPhotonsSig3 + "("+"%.1f"%float(100.0*n_nPhotonsSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ MET filters & "+"%.0f" % n_MET_filterData+"("+"%.1f"%float(100.0*n_MET_filterData/n_blindData)+"\\%)  & "+"%.2f"%n_MET_filterSig1 + "("+"%.1f"%float(100.0*n_MET_filterSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_MET_filterSig2 + "("+"%.1f"%float(100.0*n_MET_filterSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_MET_filterSig3 + "("+"%.1f"%float(100.0*n_MET_filterSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"
print >> f1,  "+ trigger path& "+"%.0f" % n_triggerData+"("+"%.1f"%float(100.0*n_triggerData/n_blindData)+"\\%)  & "+"%.2f"%n_triggerSig1 + "("+"%.1f"%float(100.0*n_triggerSig1/N_beforePreselection_Sig1)+"\\%) & "+"%.2f"%n_triggerSig2 + "("+"%.1f"%float(100.0*n_triggerSig2/N_beforePreselection_Sig2)+"\\%) & "+"%.2f"%n_triggerSig3 + "("+"%.1f"%float(100.0*n_triggerSig3/N_beforePreselection_Sig3)+"\\%) "+"\\\\"

