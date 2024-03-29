########################################################
##common configuration parameters for all plot scripts##
########################################################

#######################input trees######################
fileNameData = '/storage/user/qnguyen/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2016/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root'
fileNameGJets = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCD = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	


#fileNameSig = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root'
fileNameSig = '/storage/user/qnguyen/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2016/skim_noBDT/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root'
sigLegend = "signal (L250TeV-Ctau200cm)"
#fileNameSig = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GMSB_Ctau2190mm.root'
#sigLegend = "GMSB (2190mm)"

################lumi and cross sections#################
#lumi =  26930 #pb^-1 #2018ABC. For 2018D it's 31947 pb^-1
lumi =  31947 #pb^-1 #2018ABC. For 2018D it's 31947 pb^-1
xsecSig = 0.01262 #pb 0.0015
xsecGJets = [20790.0, 9238.0, 2305, 274.4, 93.46] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Gamma_jets
xsecQCD = [1712000, 347700, 32100, 6831, 1207, 119.9, 25.24] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
fractionGJets = 0.5271*0.92 # from fit to SigmaIetaIeta
fractionQCD = 0.4729*0.92 # from fit fo SigmaIetaIeta
useFraction = True
kFactor = 1.0
timeShift = 0.297

###############cuts and outputs########################
cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"
cut_MET_filter2 = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"
#cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"

cut = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0"
cut_trigger2g = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 8.0 && pho2hcalPFClusterIso < 8.0 && (pho2sumNeutralHadronEt*(1.0-pho2isStandardPhoton) < 30.0) && (pho2trkSumPtHollowConeDR03 < 8.0 )&& abs(pho2Eta) <2.0 && pho2R9 > 0.65"
cutHT = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0 && (HT - pho1Pt - pho2Pt > 400.0)"
cutHT_trigger2g = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 8.0 && pho2hcalPFClusterIso < 8.0 && (pho2sumNeutralHadronEt*(1.0-pho2isStandardPhoton) < 30.0) && (pho2trkSumPtHollowConeDR03 < 8.0 )&& abs(pho2Eta) <2.0 && pho2R9 > 0.65 && (HT - pho1Pt - pho2Pt > 400.0)"

cut2 = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter2 + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0 "
cut2_trigger2g = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter2 + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 8.0 && pho2hcalPFClusterIso < 8.0 && (pho2sumNeutralHadronEt*(1.0-pho2isStandardPhoton) < 30.0) && (pho2trkSumPtHollowConeDR03 < 8.0 )&& abs(pho2Eta) <2.0 && pho2R9 > 0.65"
cut2HT = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter2 + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0 && (HT - pho1Pt - pho2Pt > 400.0)"
cut2HT_trigger2g = 'pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter2 + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 8.0 && pho2hcalPFClusterIso < 8.0 && (pho2sumNeutralHadronEt*(1.0-pho2isStandardPhoton) < 30.0) && (pho2trkSumPtHollowConeDR03 < 8.0 )&& abs(pho2Eta) <2.0 && pho2R9 > 0.65 && (HT - pho1Pt - pho2Pt > 400.0)"
cut_blindMET = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && t1MET < 200.0 && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_blindTime = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1ClusterTime_SmearToData < 3.0 && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_noSminor = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_noSigmaIetaIeta = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter +"&& pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"


cut_QCD_shape = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_QCD_shape_noSigmaIetaIeta = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)' + cut_MET_filter + "&& pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"

cut_GJets_shape = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && pho1isPromptPhoton' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight)"
cut_GJets_shape_noSigmaIetaIeta = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && pho1isPromptPhoton' + cut_MET_filter + "&& pho1passHoverETight)"


cut_QCD_CR = '1.0*(pho1Pt > 70 && pho1R9 > 0.5 &&  abs(pho1Eta)<1.4442 && (!pho1passIsoTight_comboIso) && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaLoose && pho1passHoverELoose&& pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_QCD_CR_noSminor = '1.0*(pho1Pt > 70 && pho1R9 > 0.5 &&  abs(pho1Eta)<1.4442 && (!pho1passIsoTight_comboIso) && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaLoose && pho1passHoverELoose && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_QCD_CR_noSigmaIetaIeta = '1.0*(pho1Pt > 70 && pho1R9 > 0.5 &&  abs(pho1Eta)<1.4442 && (!pho1passIsoTight_comboIso) && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passHoverELoose && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"


#cut_GJets = "1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets < 3  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2   && (n_Jets == 1 || (n_Jets == 2 && jet2Pt/pho1Pt < 0.2)) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter+ " && pho1passSigmaIetaIetaTight && pho1passHoverETight)"
cut_GJets = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets < 3  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_GJets_noSminor = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets < 3  && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_GJets_noSigmaIetaIeta = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets < 3  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2  ' + cut_MET_filter + " && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"

cut_EWKCR = '1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2 && nTightMuons >= 1 ' + cut_MET_filter + " && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"

weight_cut = "(weight*pileupWeight*triggerEffSFWeight*photonEffSF) * "

cut_noDisc = cut


cut_skim = "pho1Pt > 40 && abs(pho1Eta)<1.4442 && n_Jets >= 3 && HLTDecision[880] == 1 && pho1passTrackVeto" # Fix the trigger later

cut_skim_bkg = "pho1Pt > 40 && abs(pho1Eta)<1.4442 && pho1passIsoLoose_comboIso && (HLTDecision[81] == 1 || HLTDecision[100] == 1 || HLTDecision[102]==1 || HLTDecision[92] == 1 || HLTDecision[93] == 1)"

outputDir = '/storage/user/qnguyen/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/2018/output_noBDT'

############define the plot you want to make##########
##for stack plots
#xbins_MET = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 225.0, 250.0, 275.0, 300.0, 325.0, 350.0, 375.0, 400.0, 450.0, 500.0, 700.0, 1000.0]
xbins_MET = [0.0, 10.0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 225, 250, 275, 300, 325, 350, 375, 400, 450, 500, 750, 1000]
#xbins_time = [-5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15, 25]
xbins_time = [-5.0, -3, -2, -1.5, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 5, 10, 15, 25.0]

splots = []
#variable name in the tree, output plot file name, description/title, Nbins, lowX, upX, useLogy
#cut = cut_QCD_CR
#cut = cut_trigger2g
#cut2 = cut2_trigger2g
splots.append(["t1MET", "MET_log_SR_trigger2g", "#slash{E}_{T} [GeV]", 100,0,1000, True, "GeV"])
splots.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_log_SR_trigger2g", "#gamma cluster time [ns]", 100,-5.0,25.0, True, "ns"])

#splots.append(["t1MET", "MET_linear_SR_HT", "#slash{E}_{T} [GeV]", 100,0,1000, False, "ns"])
#splots.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_linear_SR_HT", "#gamma cluster time [ns]", 100,-5.0,25.0, False, "ns"])


'''
splots.append(["pho1ClusterTime", "phoTimeCluster_noSmear_log", "#gamma cluster time [ns]", 100,-15,15, True, "ns"])
splots.append(["pho1ClusterTime", "phoTimeCluster_noSmear_linear", "#gamma cluster time [ns]", 100,-15,15, False, "ns"])

splots.append(["pho1Sminor", "Sminor_linear", "S_{minor}", 50,0,1.0, False, "unit"])
splots.append(["pho1Sminor", "Sminor_log", "S_{minor}", 50,0,1.0, True, "unit"])

splots.append(["pho1R9", "pho1R9_log", "R_{9}", 100,0.5,1.0, True, "unit"])
splots.append(["pho1R9", "pho1R9_linear", "R_{9}", 100,0.5,1.0, False, "unit"])
splots.append(["sumMET", "sumMET_linear", "#Sigma E_{T} [GeV]", 100,0,8000, False, "GeV"])
splots.append(["sumMET", "sumMET_log", "#Sigma E_{T} [GeV]", 100,0,8000, True, "GeV"])

splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_linear", "#sigma_{i#eta i#eta}", 100,0.005,0.025, False, "unit"])
splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_log", "#sigma_{i#eta i#eta}", 100,0.005,0.025, True, "unit"])

splots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor_linear", "S_{minor}/S_{major}", 50,0,1.1, False, "unit"])
splots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor_log", "S_{minor}/S_{major}", 50,0,1.1, True, "unit"])
splots.append(["sqrt(pho1Sminor)/sqrt(pho1Smajor)", "SminorSqrtOverSmajorSqrt_linear", "#sqrt{S_{minor}}/#sqrt{S_{major}}", 50,0,1.1, False, "unit"])
splots.append(["sqrt(pho1Sminor)/sqrt(pho1Smajor)", "SminorSqrtOverSmajorSqrt_log", "#sqrt{S_{minor}}/#sqrt{S_{major}}", 50,0,1.1, True, "unit"])

splots.append(["pho1ecalPFClusterIso", "pho1ecalPFClusterIso_linear", "PF Cluster ECAL isolation [GeV]", 100,-0.1,30.0, False, "GeV"])
splots.append(["pho1hcalPFClusterIso", "pho1hcalPFClusterIso_linear", "PF Cluster HCAL isolation [GeV]", 100,-0.1,30.0, False, "GeV"])
splots.append(["pho1trkSumPtHollowConeDR03", "pho1trkSumPtHollowConeDR03_linear", "PF Cluster tracker isolation [GeV]", 100,-0.1,30.0, False, "GeV"])
splots.append(["pho1sumPhotonEt", "pho1sumPhotonEt_linear", "PF photon isolation [GeV]", 100,-0.1,30.0, False, "GeV"])
splots.append(["pho1sumNeutralHadronEt", "pho1sumNeutralHadronEt_linear", "PF neutral hadron isolation [GeV]", 100,-0.1,30.0, False, "GeV"])
splots.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt_linear", "PF charged hadron isolation [GeV]", 100,-0.1,30.0, False, "GeV"])
splots.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt_log", "charged isolation [GeV]", 100,-0.1,30.0, True, "GeV"])
splots.append(["pho1sigmaEOverE", "phosigmaEOverE_linear", "#sigma_{E}/E", 100,0.,0.5, False, "unit"])
splots.append(["pho1sigmaEOverE", "phosigmaEOverE_log", "#sigma_{E}/E", 100,0.,0.5, True, "unit"])
splots.append(["pho1Pt", "phoPt_linear", "p_{T}^{#gamma} [GeV]", 100,50,2000, False, "GeV"])
splots.append(["pho1Pt", "phoPt_log", "p_{T}^{#gamma} [GeV]", 100,50,2000, True, "GeV"])
splots.append(["sqrt(pho1Sminor)", "SminorSqrt_linear", "#sqrt{S_{minor}}", 50,0,1, False, "unit"])
splots.append(["sqrt(pho1Sminor)", "SminorSqrt_log", "#sqrt{S_{minor}}", 50,0,1, True, "unit"])
splots.append(["pho1Smajor", "Smajor_linear", "S_{major}", 50,0,1, False, "unit"])
splots.append(["pho1Smajor", "Smajor_log", "S_{major}", 50,0,1, True, "unit"])
splots.append(["sqrt(pho1Smajor)", "SmajorSqrt_linear", "#sqrt{S_{major}}", 50,0,1, False, "unit"])
splots.append(["sqrt(pho1Smajor)", "SmajorSqrt_log", "#sqrt{S_{major}}", 50,0,1, True, "unit"])
splots.append(["nPV", "nPV_linear", "number of vertices", 50,-0.5,49.5, False, "unit"])
splots.append(["nPV", "nPV_log", "number of vertices", 50,-0.5,49.5, True, "unit"])
splots.append(["n_Jets", "nJets_linear", "number of jets", 15,-0.5,14.5, False, "unit"])
splots.append(["n_Jets", "nJets_log", "number of jets", 15,-0.5,14.5, True, "unit"])
splots.append(["pho1Pt", "phoPt_linear", "p_{T}^{#gamma} [GeV]", 100,100,2000, False, "GeV"])
splots.append(["pho1Pt", "phoPt_log", "p_{T}^{#gamma} [GeV]", 100,100,2000, True, "GeV"])
splots.append(["pho1SeedTimeRaw", "phoTimeSeedRaw_linear", "#gamma seed raw time [ns]", 100,-15,15, False, "ns"])
splots.append(["pho1SeedTimeRaw", "phoTimeSeedRaw_log", "#gamma seed raw time [ns]", 100,-15,15, True, "ns"])
splots.append(["pho1SeedTimeCalib", "phoTimeSeedCalib_linear", "#gamma seed calibrated time [ns]", 100,-15,15, False, "ns"])
splots.append(["pho1SeedTimeCalib", "phoTimeSeedCalib_log", "#gamma seed calibrated time [ns]", 100,-15,15, True, "ns"])
splots.append(["pho1SeedTimeCalibTOF", "phoTimeSeedCalibTOF_linear", "#gamma seed calibrated time & TOF [ns]", 100,-15,15, False, "ns"])
splots.append(["pho1SeedTimeCalibTOF", "phoTimeSeedCalibTOF_log", "#gamma seed calibrated time & TOF [ns]", 100,-15,15, True, "ns"])
'''

############define the variables for which you want to save the bkg shape##########
shapes = []
shapes.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta", "#sigma_{i#eta i#eta}", 100,0.005,0.025])
shapes.append(["pho1sigmaEOverE", "phosigmaEOverE", "#sigma_{E}/E", 100,0.,0.5])
shapes.append(["pho1Smajor", "Smajor", "S_{major}", 100,0,1])
shapes.append(["pho1Sminor", "Sminor", "S_{minor}", 100,0,0.5])
shapes.append(["pho1Pt", "phoPt", "p_{T}^{#gamma} [GeV]", 100,50,1500])
shapes.append(["n_Jets", "nJets", "number of jets", 15,-0.5,14.5])

#####################limit plot settings####################################

list_limits_vs_lifetime = []

limits_vs_lifetime1 = []
limits_vs_lifetime1.append(["L150TeV_Ctau0_1cm",   150.0, 212.1, 0.1,   0.233382])
limits_vs_lifetime1.append(["L150TeV_Ctau10cm",   150.0, 212.1, 10.0,   0.23281])
limits_vs_lifetime1.append(["L150TeV_Ctau200cm",   150.0, 212.1, 200.0,   0.23355])
limits_vs_lifetime1.append(["L150TeV_Ctau400cm",   150.0, 212.1, 400.0,   0.231478])
limits_vs_lifetime1.append(["L150TeV_Ctau600cm",   150.0, 212.1, 600.0,   0.234354])
limits_vs_lifetime1.append(["L150TeV_Ctau800cm",   150.0, 212.1, 800.0,   0.230648])
limits_vs_lifetime1.append(["L150TeV_Ctau1000cm",  150.0, 212.1, 1000.0,  0.233782])
mass_limits_vs_lifetime1 = 212.1
list_limits_vs_lifetime.append([mass_limits_vs_lifetime1, limits_vs_lifetime1])


limits_vs_lifetime2 = []
limits_vs_lifetime2.append(["L200TeV_Ctau0_1cm",   200.0, 284.8, 0.1,   0.0428312])
limits_vs_lifetime2.append(["L200TeV_Ctau10cm",   200.0, 284.8, 10.0,   0.0428514])
limits_vs_lifetime2.append(["L200TeV_Ctau200cm",   200.0, 284.8, 200.0,   0.0424614])
limits_vs_lifetime2.append(["L200TeV_Ctau400cm",   200.0, 284.8, 400.0,   0.0427252])
limits_vs_lifetime2.append(["L200TeV_Ctau600cm",   200.0, 284.8, 600.0,   0.0431458])
limits_vs_lifetime2.append(["L200TeV_Ctau800cm",   200.0, 284.8, 800.0,   0.0423242])
limits_vs_lifetime2.append(["L200TeV_Ctau1000cm",   200.0, 284.8, 1000.0,   0.042969])
limits_vs_lifetime2.append(["L200TeV_Ctau1200cm",   200.0, 284.8, 1200.0,   0.0422256])
mass_limits_vs_lifetime2 = 284.8
list_limits_vs_lifetime.append([mass_limits_vs_lifetime2, limits_vs_lifetime2])


limits_vs_lifetime3 = []
limits_vs_lifetime3.append(["L250TeV_Ctau10cm",   250.0, 357.5, 10.0,   0.0116892])
limits_vs_lifetime3.append(["L250TeV_Ctau200cm",   250.0, 357.5, 200.0,   0.0118048])
limits_vs_lifetime3.append(["L250TeV_Ctau400cm",  250.0, 357.5, 400.0,  0.0115646])
limits_vs_lifetime3.append(["L250TeV_Ctau600cm",  250.0, 357.5, 600.0,  0.0116992])
limits_vs_lifetime3.append(["L250TeV_Ctau800cm",  250.0, 357.5, 800.0,  0.0116992])
limits_vs_lifetime3.append(["L250TeV_Ctau1000cm",  250.0, 357.5, 1000.0,  0.0116992])
limits_vs_lifetime3.append(["L250TeV_Ctau1200cm",  250.0, 357.5, 1200.0,  0.0116992])
mass_limits_vs_lifetime3 = 357.5
list_limits_vs_lifetime.append([mass_limits_vs_lifetime3, limits_vs_lifetime3])

limits_vs_lifetime4 = []
limits_vs_lifetime4.append(["L300TeV_Ctau0_1cm",  300.0, 430.4, 0.1,  0.00418322])
limits_vs_lifetime4.append(["L300TeV_Ctau10cm",  300.0, 430.4, 10.0,  0.00410951])
limits_vs_lifetime4.append(["L300TeV_Ctau200cm",  300.0, 430.4, 200.0,  0.00418529])
limits_vs_lifetime4.append(["L300TeV_Ctau400cm",  300.0, 430.4, 400.0,  0.00418529])
limits_vs_lifetime4.append(["L300TeV_Ctau600cm",  300.0, 430.4, 600.0,  0.0041645])
limits_vs_lifetime4.append(["L300TeV_Ctau800cm",  300.0, 430.4, 800.0,  0.0041645])
limits_vs_lifetime4.append(["L300TeV_Ctau1000cm",  300.0, 430.4, 1000.0,  0.0041645])
limits_vs_lifetime4.append(["L300TeV_Ctau1200cm",  300.0, 430.4, 1200.0,  0.0041645])
mass_limits_vs_lifetime4 = 430.4
list_limits_vs_lifetime.append([mass_limits_vs_lifetime4, limits_vs_lifetime4])


list_limits_vs_mass = []

limits_vs_mass1 = []
limits_vs_mass1.append(["L100TeV_Ctau1200cm", 100.0, 139.4, 1200.0, 2.09996])
limits_vs_mass1.append(["L200TeV_Ctau1200cm",   200.0, 284.8, 1200.0,   0.0422256])
limits_vs_mass1.append(["L250TeV_Ctau1200cm",   250.0, 357.5, 1200.0,   0.0116992])
limits_vs_mass1.append(["L300TeV_Ctau1200cm",   300.0, 430.4, 1200.0,   0.0041645])
limits_vs_mass1.append(["L350TeV_Ctau1200cm",   350.0, 503.4, 1200.0,   0.00174708])
limits_vs_mass1.append(["L400TeV_Ctau1200cm",   400.0, 576.4, 1200.0,   0.000793036])
lifetime_limits_vs_mass1 = 1200.0
list_limits_vs_mass.append([lifetime_limits_vs_mass1, limits_vs_mass1])


limits_vs_mass2 = []
limits_vs_mass2.append(["L100TeV_Ctau600cm",   100.0, 139.4, 600.0,   2.07166])
limits_vs_mass2.append(["L150TeV_Ctau600cm",   150.0, 212.1, 600.0,   0.234354])
limits_vs_mass2.append(["L200TeV_Ctau600cm",   200.0, 284.8, 600.0,   0.0431458])
limits_vs_mass2.append(["L250TeV_Ctau600cm",  250.0, 357.5, 600.0,  0.0116992])
limits_vs_mass2.append(["L300TeV_Ctau600cm",  300.0, 430.4, 600.0,  0.0041645])
limits_vs_mass2.append(["L350TeV_Ctau600cm",  300.0, 503.4, 600.0,  0.00174708])
limits_vs_mass2.append(["L400TeV_Ctau600cm",  300.0, 576.4, 600.0,  0.000790256])
lifetime_limits_vs_mass2 = 600.0
list_limits_vs_mass.append([lifetime_limits_vs_mass2, limits_vs_mass2])


limits_vs_mass3 = []
limits_vs_mass3.append(["L100TeV_Ctau200cm",   100.0, 139.4, 200.0,   2.07166])
limits_vs_mass3.append(["L150TeV_Ctau200cm",   150.0, 212.1, 200.0,   0.23555])
limits_vs_mass3.append(["L200TeV_Ctau200cm",   200.0, 284.8, 200.0,   0.0424614])
limits_vs_mass3.append(["L250TeV_Ctau200cm",   250.0, 357.5, 200.0,   0.0118048])
limits_vs_mass3.append(["L300TeV_Ctau200cm",   300.0, 430.4, 200.0,  0.00418529])
limits_vs_mass3.append(["L350TeV_Ctau200cm",   350.0, 503.4, 200.0,   0.00174708])
limits_vs_mass3.append(["L400TeV_Ctau200cm",   400.0, 576.4, 200.0,   0.000790256])
lifetime_limits_vs_mass3 = 200.0
list_limits_vs_mass.append([lifetime_limits_vs_mass3, limits_vs_mass3])

limits_vs_mass4 = []
limits_vs_mass4.append(["L100TeV_Ctau0_1cm",   100.0, 139.4, 0.1,   2.07166])
limits_vs_mass4.append(["L150TeV_Ctau0_1cm",   150.0, 212.1, 0.1,   0.233382])
limits_vs_mass4.append(["L200TeV_Ctau0_1cm",   200.0, 284.8, 0.1,   0.0428312])
limits_vs_mass4.append(["L300TeV_Ctau0_1cm",  300.0, 430.4, 0.1,  0.00418322])
limits_vs_mass4.append(["L350TeV_Ctau0_1cm",  350.0, 503.4, 0.1,  0.00172168])
limits_vs_mass4.append(["L400TeV_Ctau0_1cm",  400.0, 576.4, 0.1,  0.000798117])
lifetime_limits_vs_mass4 = 0.1
list_limits_vs_mass.append([lifetime_limits_vs_mass4, limits_vs_mass4])

limits_vs_mass5 = []
limits_vs_mass5.append(["L100TeV_Ctau10cm",   100.0, 139.4, 10.0,   2.07166])
limits_vs_mass5.append(["L150TeV_Ctau10cm",   150.0, 212.1, 10.0,   0.23281])
limits_vs_mass5.append(["L200TeV_Ctau10cm",   200.0, 284.8, 10.0,   0.0428512])
limits_vs_mass5.append(["L250TeV_Ctau10cm",   250.0, 357.5, 10.0,   0.0118188])
limits_vs_mass5.append(["L300TeV_Ctau10cm",  300.0, 430.4, 10.0,  0.00413536])
limits_vs_mass5.append(["L350TeV_Ctau10cm",  350.0, 503.4, 10.0,  0.00172168])
limits_vs_mass5.append(["L400TeV_Ctau10cm",  400.0, 576.4, 10.0,  0.000790256])
lifetime_limits_vs_mass5 = 10.0
list_limits_vs_mass.append([lifetime_limits_vs_mass5, limits_vs_mass5])

limits_vs_mass6 = []
limits_vs_mass6.append(["L100TeV_Ctau400cm",   100.0, 139.4, 400.0,   2.07166])
limits_vs_mass6.append(["L150TeV_Ctau400cm",   150.0, 212.1, 400.0,   0.23555])
limits_vs_mass6.append(["L200TeV_Ctau400cm",   200.0, 284.8, 400.0,   0.0424614])
limits_vs_mass6.append(["L250TeV_Ctau400cm",   250.0, 357.5, 400.0,   0.0118048])
limits_vs_mass6.append(["L300TeV_Ctau400cm",   300.0, 430.4, 400.0,  0.00418529])
limits_vs_mass6.append(["L350TeV_Ctau400cm",   350.0, 503.4, 400.0,   0.00174708])
limits_vs_mass6.append(["L400TeV_Ctau400cm",   400.0, 576.4, 400.0,   0.000790256])
lifetime_limits_vs_mass6 = 400.0
list_limits_vs_mass.append([lifetime_limits_vs_mass6, limits_vs_mass6])

limits_vs_mass7 = []
limits_vs_mass7.append(["L150TeV_Ctau800cm",   150.0, 212.1, 800.0,   0.23555])
limits_vs_mass7.append(["L200TeV_Ctau800cm",   200.0, 284.8, 800.0,   0.0424614])
limits_vs_mass7.append(["L250TeV_Ctau800cm",   250.0, 357.5, 800.0,   0.0118048])
limits_vs_mass7.append(["L300TeV_Ctau800cm",   300.0, 430.4, 800.0,  0.00418529])
limits_vs_mass7.append(["L350TeV_Ctau800cm",   350.0, 503.4, 800.0,   0.00174708])
limits_vs_mass7.append(["L400TeV_Ctau800cm",   400.0, 576.4, 800.0,   0.000790256])
lifetime_limits_vs_mass7 = 800.0
list_limits_vs_mass.append([lifetime_limits_vs_mass7, limits_vs_mass7])

limits_vs_mass8 = []
limits_vs_mass8.append(["L100TeV_Ctau1000cm",   100.0, 139.4, 1000.0,   2.07166])
limits_vs_mass8.append(["L150TeV_Ctau1000cm",   150.0, 212.1, 1000.0,   0.23555])
limits_vs_mass8.append(["L200TeV_Ctau1000cm",   200.0, 284.8, 1000.0,   0.0424614])
limits_vs_mass8.append(["L250TeV_Ctau1000cm",   250.0, 357.5, 1000.0,   0.0118048])
limits_vs_mass8.append(["L300TeV_Ctau1000cm",   300.0, 430.4, 1000.0,  0.00418529])
limits_vs_mass8.append(["L350TeV_Ctau1000cm",   350.0, 503.4, 1000.0,   0.00174708])
limits_vs_mass8.append(["L400TeV_Ctau1000cm",   400.0, 576.4, 1000.0,   0.000790256])
lifetime_limits_vs_mass8 = 1000.0
list_limits_vs_mass.append([lifetime_limits_vs_mass8, limits_vs_mass8])


exclusion_region_2D = []
exclusion_region_2D.append(["L100TeV_Ctau0_1cm", 100.0, 139.4, 0.1, 2.07166])
exclusion_region_2D.append(["L100TeV_Ctau10cm", 100.0, 139.4, 10.0, 2.07166])
exclusion_region_2D.append(["L100TeV_Ctau200cm", 100.0, 139.4, 200.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau400cm", 100.0, 139.4, 400.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau600cm", 100.0, 139.4, 600.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau1000cm", 100.0, 139.4, 1000.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau1200cm", 100.0, 139.4, 1200.0, 2.09996])
exclusion_region_2D.append(["L150TeV_Ctau0_1cm",   150.0, 212.1, 0.1,   0.233382])
exclusion_region_2D.append(["L150TeV_Ctau10cm",   150.0, 212.1, 10.0,   0.23281])
exclusion_region_2D.append(["L150TeV_Ctau200cm",   150.0, 212.1, 200.0,   0.23355])
exclusion_region_2D.append(["L150TeV_Ctau400cm",   150.0, 212.1, 400.0,   0.231478])
exclusion_region_2D.append(["L150TeV_Ctau600cm",   150.0, 212.1, 600.0,   0.234354])
exclusion_region_2D.append(["L150TeV_Ctau800cm",   150.0, 212.1, 800.0,   0.230648])
exclusion_region_2D.append(["L150TeV_Ctau1000cm",  150.0, 212.1, 1000.0,  0.233782])
exclusion_region_2D.append(["L200TeV_Ctau0_1cm",   200.0, 284.8, 0.1,   0.0428312])
exclusion_region_2D.append(["L200TeV_Ctau10cm",   200.0, 284.8, 10.0,   0.0428512])
exclusion_region_2D.append(["L200TeV_Ctau200cm",   200.0, 284.8, 200.0,   0.0424614])
exclusion_region_2D.append(["L200TeV_Ctau400cm",   200.0, 284.8, 400.0,   0.0427252])
exclusion_region_2D.append(["L200TeV_Ctau600cm",   200.0, 284.8, 600.0,   0.0431458])
exclusion_region_2D.append(["L200TeV_Ctau800cm",   200.0, 284.8, 800.0,   0.0423242])
exclusion_region_2D.append(["L200TeV_Ctau1000cm",   200.0, 284.8, 1000.0,   0.042969])
exclusion_region_2D.append(["L200TeV_Ctau1200cm",   200.0, 284.8, 1200.0,   0.0422256])
exclusion_region_2D.append(["L250TeV_Ctau10cm",   250.0, 357.5, 10.0,   0.0118188])
exclusion_region_2D.append(["L250TeV_Ctau200cm",  250.0, 357.5, 200.0,  0.0118048])
exclusion_region_2D.append(["L250TeV_Ctau400cm",   250.0, 357.5, 400.0,   0.0115646])
exclusion_region_2D.append(["L250TeV_Ctau600cm",  250.0, 357.5, 600.0,  0.0116992])
exclusion_region_2D.append(["L250TeV_Ctau800cm",  250.0, 357.5, 800.0,  0.0116992])
exclusion_region_2D.append(["L250TeV_Ctau1000cm",  250.0, 357.5, 1000.0,  0.0116992])
exclusion_region_2D.append(["L250TeV_Ctau1200cm",  250.0, 357.5, 1200.0,  0.0116992])
exclusion_region_2D.append(["L300TeV_Ctau0_1cm",  300.0, 430.4, 0.1,  0.00418322])
exclusion_region_2D.append(["L300TeV_Ctau10cm",  300.0, 430.4, 10.0,  0.00413536])
exclusion_region_2D.append(["L300TeV_Ctau200cm",  300.0, 430.4, 200.0,  0.00418529])
exclusion_region_2D.append(["L300TeV_Ctau400cm",  300.0, 430.4, 400.0,  0.00418529])
exclusion_region_2D.append(["L300TeV_Ctau600cm",  300.0, 430.4, 600.0,  0.0041645])
exclusion_region_2D.append(["L300TeV_Ctau800cm",  300.0, 430.4, 800.0,  0.0041645])
exclusion_region_2D.append(["L300TeV_Ctau1000cm",  300.0, 430.4, 1000.0,  0.0041645])
exclusion_region_2D.append(["L300TeV_Ctau1200cm",  300.0, 430.4, 1200.0,  0.0041645])
exclusion_region_2D.append(["L350TeV_Ctau0_1cm",  350.0, 503.4, 0.1,  0.00172168])
exclusion_region_2D.append(["L350TeV_Ctau10cm",  350.0, 503.4, 10.0,  0.00172168])
exclusion_region_2D.append(["L350TeV_Ctau200cm",  350.0, 503.4, 200.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau400cm",  350.0, 503.4, 400.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau600cm",  350.0, 503.4, 600.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau800cm",  350.0, 503.4, 800.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau1000cm",  350.0, 503.4, 1000.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau1200cm",  350.0, 503.4, 1200.0,  0.00174708])
exclusion_region_2D.append(["L400TeV_Ctau0_1cm",   400.0, 576.4, 0.1,   0.000798117])
exclusion_region_2D.append(["L400TeV_Ctau10cm",   400.0, 576.4, 10.0,   0.000798117])
exclusion_region_2D.append(["L400TeV_Ctau200cm",  400.0, 576.4, 200.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau400cm",  400.0, 576.4, 400.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau600cm",  400.0, 576.4, 600.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau800cm",  400.0, 576.4, 800.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau1000cm",  400.0, 576.4, 1000.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau1200cm",  400.0, 576.4, 1200.0,  0.000793036])

grid_mass_exclusion_region_2D = [0.0, 139.4, 212.1, 284.8, 357.5, 430.4, 503.4, 576.4]
grid_lambda_exclusion_region_2D = [0.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0]
#grid_lifetime_exclusion_region_2D = [20000.0, 4000.0, 1200.0, 1000.0, 800.0, 600.0, 400.0, 200.0, 100.0, 60.0, 50.0, 25.0, 10.0, 5.0, 1.0, 0.5, 0.1, 0.01, 0.0]
grid_lifetime_exclusion_region_2D = [4000.0, 1200.0, 1000.0, 800.0, 600.0, 400.0, 200.0, 100.0, 50.0, 10.0, 5.0, 0.1, 0.01, 0.0]


#############################input files to skim script#####################

fileNameDataSkim = [
        '/storage/af/user/qnguyen/DelayedPhoton/CMSSW_10_6_12/src/DelayedPhotonID/deployment/output_bothpho_2018D/DelayedPhoton_EGamma_Run2018D.root',
        ]


fileNameSigSkim_this = ['/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/reproduce/hadd/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root']

fileNameSigSkim = [
'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_EGamma_Run2018B.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-10000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-400cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_EGamma_Run2018D.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-300TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-250TeV_Ctau-10cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-450TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_DiPhotonJetsBox_M40_80-Sherpa.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_EGamma_Run2018A.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-150TeV_Ctau-800cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-100cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-1000cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-350TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-100TeV_Ctau-50cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_EGamma_Run2018C.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-200TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-1200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-500TeV_Ctau-200cm_TuneCP5_13TeV-pythia8.root'
,'/storage/af/user/yeseo/DelayedPhoton/CMSSW_10_6_20/src/DelayedPhotonID/deployment/output_bothpho_2018/DelayedPhoton_GMSB_L-400TeV_Ctau-600cm_TuneCP5_13TeV-pythia8.root'
        ]

