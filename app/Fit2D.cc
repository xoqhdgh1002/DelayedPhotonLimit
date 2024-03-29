//C++ INCLUDES
#include <iostream>
#include <sys/stat.h>
#include <vector>
//ROOT INCLUDES
#include <TFile.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TROOT.h>
#include <THStack.h>
#include <TStyle.h>
#include <TColor.h>
//LOCAL INCLUDES
#include "MakeFitMETTime.hh"
#include "Aux.hh"

using namespace std;

Int_t Nbins_MET = 15;
Int_t Nbins_MET_lowT = 6;
Int_t Nbins_MET_highT = 5;
Int_t Nbins_time = 20;
Int_t Nbins_time_lowT = 5;
Int_t Nbins_time_highT = 7;
Int_t Nbins_total = Nbins_MET*Nbins_time;
Double_t xbins_MET[16] = {0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0};
//Double_t xbins_MET_lowT[16] = {0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0};
//Double_t xbins_MET_highT[16] = {0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0};
Double_t xbins_MET_lowT[7] = {0.0, 70, 130, 225.0, 295.0, 320.0, 1000.0};
Double_t xbins_MET_highT[6] = {0.0, 55.0, 85.0, 185.0, 500.0, 1000.0};
Double_t xbins_time[21] = {-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15};
//Double_t xbins_time_lowT[21] = {-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15};
//Double_t xbins_time_highT[21] = {-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15};
Double_t xbins_time_lowT[6] = {-15.0, -0.7, 0.3, 0.8, 1.4, 15.0};
Double_t xbins_time_highT[8] = {-15.0, -0.7, 0.0, 0.9, 1.6, 3.0, 10.0, 15.0};

bool useLowTBinning = false;
bool useBDT = true;

float lumi = 35922.0; //pb^-1
float NEvents_sig = 1.0;
bool _useToy = true;

bool doAllBkgFracFit = false;

int main( int argc, char* argv[])
{
srand(time(NULL));
gROOT->Reset();
gROOT->SetBatch(1);
gStyle->SetOptStat(0);
gStyle->SetOptFit(111);
gStyle->SetPalette(1);

std::string inputFileName_data = argv[1];
std::string inputFileName_signal = argv[2];
std::string sigModelName = argv[3]; 
std::string sigModelTitle = argv[4]; 
std::string category = argv[5];
std::string fitMode = argv[6]; //options: "datacard", "bias"
std::string s_useBDT = argv[7]; //options: "datacard", "bias"
std::string _SoverB = "";
std::string _nToys = "";

if(fitMode == "bias" && argc >= 9) _SoverB = argv[8]; 
if(fitMode == "bias" && argc >= 10) _nToys = argv[9]; 


if(s_useBDT == "")
{
        std::cerr << "[ERROR]: please provide the photon ID choice - whether useBDT or not (yes or no)" << std::endl;
        return -1;
}
else if (s_useBDT == "yes")
{
	useBDT = true;
	cout<<"photon ID: BDT"<<endl;
}
else if (s_useBDT == "no")
{
	useBDT = false;
	cout<<"photon ID: EGM cut-based"<<endl;
}
else
{
	std::cerr << "[ERROR]: please provide the photon ID choice - whether useBDT or not (yes or no)" << std::endl;
        return -1;
}


float SoverB = 0.0;
int nToys = 1000;

if (sigModelName.find("0p") != std::string::npos || sigModelName.find("5cm") != std::string::npos || sigModelName.find("10cm") != std::string::npos || sigModelName.find("50cm") != std::string::npos) useLowTBinning = true;

if(useLowTBinning)
{
	Nbins_MET = Nbins_MET_lowT;
	Nbins_time = Nbins_time_lowT;
	Nbins_total = Nbins_MET_lowT*Nbins_time_lowT;
}
else
{
	Nbins_MET = Nbins_MET_highT;
	Nbins_time = Nbins_time_highT;
	Nbins_total = Nbins_MET_highT*Nbins_time_highT;
}

TString _sigModelName (sigModelName.c_str());
TString _sigModelTitle (sigModelTitle.c_str());

float xsec = getXsecBR(sigModelName); //pb
std::string treeName = "DelayedPhoton";

std::string cut, cut_JESUp, cut_JESDown, cut_noHLT, cut_loose, cut_GJets, cut_noSigmaIetaIeta;

std::string weight_cut = "weight*pileupWeight*triggerEffSFWeight*photonEffSF*triggerEffWeight*";

std::string cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0" ;

std::string cut_pho1Tight = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && pho1SigmaIetaIeta < 0.00994";
std::string cut_pho1Tight_GJets = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1SigmaIetaIeta < 0.00994";
std::string cut_pho1Tight_noSigmaIetaIeta = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3";
std::string cut_pho1Loose = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.7 && pho1SigmaIetaIeta < 0.01031";
std::string cut_pho1Loose_noSigmaIetaIeta = " && pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.7";
std::string cut_EWKCR = "(abs(lep1Type) == 11 || abs(lep1Type) == 13) && (abs(lep2Type) == 11 || abs(lep2Type) == 13) && lep1Pt > 30 && lep2Pt>30 && mll > 20 && ((abs(lep1Type) != abs(lep2Type)) || (mll < 76 || mll > 106))  && t1MET > 40";


if(category == "2J")
{
	if(!useBDT)
	{
		cut_noSigmaIetaIeta = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight_noSigmaIetaIeta;
		cut = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESUp = "n_Jets_JESUp == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESDown = "n_Jets_JESDown == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_noHLT = "n_Jets == 2 && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_loose = "n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Loose;
		cut_GJets = "n_Jets == 1 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)&& (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
	}
	else
	{
		cut_noSigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESUp = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESUp == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESDown = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESDown == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_noHLT = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets == 2 && n_Photons == 2 " + cut_MET_filter;
		cut_loose = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.0586 && pho1passEleVeto && n_Jets == 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_GJets = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets == 1 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter;
	}
}

else if(category == "3J")
{
	if(!useBDT)
	{
		cut_noSigmaIetaIeta = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight_noSigmaIetaIeta;
		cut = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESUp = "n_Jets_JESUp > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_JESDown = "n_Jets_JESDown > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_noHLT = "n_Jets > 2 && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
		cut_loose = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Loose;
		cut_GJets = "n_Jets < 3 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)&& (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter + cut_pho1Tight;
	}
	else
	{
		cut_noSigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESUp = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESUp > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_JESDown = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets_JESDown > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_noHLT = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets > 2 && n_Photons == 2 " + cut_MET_filter;
		cut_loose = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.0586 && pho1passEleVeto && n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 " + cut_MET_filter;
		cut_GJets = "pho1Pt > 70 && abs(pho1Eta)<1.44 && disc > 0.10 && pho1passEleVeto && n_Jets < 3 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter;
	}
}

else
{
	std::cerr << "[ERROR]: please provide a valid category: 2J or 3J" << std::endl;
	return -1;
}

cut_GJets = "weight_sumET * ("+cut_GJets+")";

cout<<"cut --> "<<cut<<endl;
cout<<"cut_loose --> "<<cut_loose<<endl;
cout<<"cut_GJets --> "<<cut_GJets<<endl;
cout<<"cut_QCD --> "<<cut_loose + " && ! (" + cut + ")"<<endl;

TString outPlotsDir;
if(category == "2J" && useBDT ) outPlotsDir = "plots_2J_withBDT";
if(category == "2J" && !useBDT ) outPlotsDir = "plots_2J_noBDT";
if(category == "3J" && useBDT ) outPlotsDir = "plots_3J_withBDT";
if(category == "3J" && !useBDT ) outPlotsDir = "plots_3J_noBDT";
std::string _outPlotsDir (((const char*) outPlotsDir));

TString outBinningDir;
if(category == "2J" && useBDT) outBinningDir == "binning_2J_withBDT";
if(category == "2J" && !useBDT) outBinningDir == "binning_2J_noBDT";
if(category == "3J" && useBDT) outBinningDir == "binning_3J_withBDT";
if(category == "3J" && !useBDT) outBinningDir == "binning_3J_noBDT";
std::string _outBinningDir ((const char*) outBinningDir);

TString outDataCardsDir;
if(category == "2J" && useBDT) outDataCardsDir = "datacards_2J_withBDT";
if(category == "2J" && !useBDT) outDataCardsDir = "datacards_2J_noBDT";
if(category == "3J" && useBDT) outDataCardsDir = "datacards_3J_withBDT";
if(category == "3J" && !useBDT) outDataCardsDir = "datacards_3J_noBDT";
std::string _outDataCardsDir ((const char*) outDataCardsDir);	

TString outBiasDir;
if(category == "2J" && useBDT) outBiasDir = "bias_2J_withBDT";
if(category == "2J" && !useBDT) outBiasDir = "bias_2J_noBDT";
if(category == "3J" && useBDT) outBiasDir = "bias_3J_withBDT";
if(category == "3J" && !useBDT) outBiasDir = "bias_3J_noBDT";
std::string _outBiasDir ((const char*) outBiasDir);
	
if(inputFileName_data == "")
{
	std::cerr << "[ERROR]: please provide an input file for data" << std::endl;
	return -1;
}
std::cout<<"using input file for data: "<<inputFileName_data<<std::endl;

if(inputFileName_signal == "")
{
	std::cerr << "[ERROR]: please provide an input file for signal" << std::endl;
	return -1;
}

if(sigModelName == "")
{
	std::cerr << "[ERROR]: please provide the name of the signal model" << std::endl;
	return -1;
}

if(sigModelTitle == "")
{
	std::cerr << "[ERROR]: please provide the title of the signal model" << std::endl;
	return -1;
}

if(fitMode == "")
{
	std::cerr << "[ERROR]: please provide the fit mode (datacard or bias)" << std::endl;
	return -1;
}

std::cout<<"using input file for data: "<<inputFileName_data<<std::endl;
std::cout<<"using input file for signal: "<<inputFileName_signal<<std::endl;
std::cout<<"signal model: "<<sigModelName<<std::endl;
std::cout<<"signal title: "<<sigModelTitle<<std::endl;
std::cout<<"fit mode: "<<fitMode<<std::endl;

if(fitMode == "bias")
{
	if(_SoverB == "")
	{
		cout<<" bias test: SoverB not specified, setting to default: 0"<<endl;
	}
	else
	{
		SoverB = strtof(_SoverB.c_str(), 0);
		cout<<"bias test: SoverB ="<<SoverB<<endl;
	}

	if(_nToys == "")
	{
		cout<<" bias test: nToys not specified, setting to default: 1000"<<endl;
	}
	else
	{
		nToys = stoi(_nToys.c_str(), 0);
		cout<<"bias test: nToys ="<<nToys<<endl;
	}

}

std::cout<<"signal xsec*BR = "<<xsec<<endl;

TFile *file_data;
TFile *file_signal;

TTree *tree_data;
TTree *tree_signal;

std::cout<<"reading data file......"<<endl;
file_data = new TFile(inputFileName_data.c_str(), "READ");
tree_data = (TTree*)file_data->Get(treeName.c_str());

std::cout<<"reading signal file......"<<endl;
file_signal = new TFile(inputFileName_signal.c_str(), "READ");
tree_signal = (TTree*)file_signal->Get(treeName.c_str());

TH1F *h1_NEvents_sig = (TH1F*) file_signal->Get("NEvents");
NEvents_sig = h1_NEvents_sig->GetBinContent(1);

//EWK background MC samples
std::vector <std::string> sample_EWK;
std::vector <float> xsec_EWK;
std::vector <TTree*> trees_EWK;
std::vector <float> NEvents_EWK;

ifstream is_EWK_list("data/EWK_bkg.list");
std::string prefix_filename_EWK;
is_EWK_list>>prefix_filename_EWK;

while(!is_EWK_list.eof())
{
	std::string sample_name_EWK_thisline;
	std::string xsec_EWK_thisline;
	is_EWK_list>>sample_name_EWK_thisline;
	is_EWK_list>>xsec_EWK_thisline;
	
	//cout<<sample_name_EWK_thisline<<" "<<xsec_EWK_thisline<<endl;	

	if(sample_name_EWK_thisline != "")
	{	
		sample_EWK.push_back(sample_name_EWK_thisline);
		xsec_EWK.push_back(strtof(xsec_EWK_thisline.c_str(), 0));
		TFile * file_EWK_this = new TFile((prefix_filename_EWK+sample_name_EWK_thisline+".root").c_str(), "READ");
		trees_EWK.push_back((TTree*)file_EWK_this->Get(treeName.c_str()));
		TH1F * h1_EWK_NEvents_this =  (TH1F*)file_EWK_this->Get("NEvents");
		NEvents_EWK.push_back(h1_EWK_NEvents_this->GetBinContent(1));	
	}
	
}

//debug
cout<<"Reading EWK list.... sample - xsec - NEvents - NEntries : "<<endl;
for(int i=0; i<xsec_EWK.size(); i++)
{
	cout<<sample_EWK[i]<<"   "<<xsec_EWK[i]<<"   "<<NEvents_EWK[i]<<"   "<<trees_EWK[i]->GetEntries()<<endl;
}

std::cout<<"reading shape file......"<<endl;
std::string shape_file_name;
if (category=="2J" && useBDT) shape_file_name = "data/shapes_2J_withBDT.root";
if (category=="2J" && !useBDT) shape_file_name = "data/shapes_2J_noBDT.root";
if (category=="3J" && useBDT) shape_file_name = "data/shapes_3J_withBDT.root";
if (category=="3J" && !useBDT) shape_file_name = "data/shapes_3J_noBDT.root";

TFile *file_shape = new TFile(shape_file_name.c_str(),"READ");

mkdir("fit_results", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016/plots_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016/plots_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016/plots_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
mkdir("fit_results/2016/plots_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);

TFile *f_Out = new TFile(("fit_results/2016/"+_outPlotsDir+"/fit_ws_"+sigModelName+".root").c_str(),"recreate");

int N_obs_total = tree_data->CopyTree( cut.c_str() )->GetEntries();
float N_total_GJets_QCD_fit = 0.0;

/**********fit to get relative yield of GJets and QCD backgrounds *****/
//SigmaIetaIeta
std::cout<<"performing SigmaIetaIeta fit......"<<endl;
TH1F *h1_SigmaIetaIeta_Data = new TH1F("h1_SigmaIetaIeta_Data","h1_SigmaIetaIeta_Data", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_Data", cut_noSigmaIetaIeta.c_str());

TH1F *h1_SigmaIetaIeta_GJets = (TH1F*)file_shape->Get("phoSigmaIetaIeta_histGJets"); 
TH1F *h1_SigmaIetaIeta_QCD = (TH1F*)file_shape->Get("phoSigmaIetaIeta_histQCD"); 

h1_SigmaIetaIeta_GJets->Scale((1.0*h1_SigmaIetaIeta_Data->Integral())/h1_SigmaIetaIeta_GJets->Integral());
h1_SigmaIetaIeta_QCD->Scale((1.0*h1_SigmaIetaIeta_Data->Integral())/h1_SigmaIetaIeta_QCD->Integral());

RooWorkspace * w_frac_SigmaIetaIeta;
w_frac_SigmaIetaIeta = FitDataBkgFraction(h1_SigmaIetaIeta_Data, "pho1SigmaIetaIeta", "#sigma_{i#etai#eta}", "", lumi, 0.005, 0.025, h1_SigmaIetaIeta_GJets, h1_SigmaIetaIeta_QCD, outPlotsDir);
w_frac_SigmaIetaIeta->Write("w_frac_SigmaIetaIeta");

float nGJets_value_SigmaIetaIeta = w_frac_SigmaIetaIeta->var("nGJets")->getValV();
float nGJets_value_SigmaIetaIeta_err = w_frac_SigmaIetaIeta->var("nGJets")->getError();
float nQCD_value_SigmaIetaIeta = w_frac_SigmaIetaIeta->var("nQCD")->getValV();
float nQCD_value_SigmaIetaIeta_err = w_frac_SigmaIetaIeta->var("nQCD")->getError();
h1_SigmaIetaIeta_GJets->Scale(nGJets_value_SigmaIetaIeta);
h1_SigmaIetaIeta_QCD->Scale(nQCD_value_SigmaIetaIeta);
h1_SigmaIetaIeta_GJets->Write();
h1_SigmaIetaIeta_QCD->Write();

N_total_GJets_QCD_fit = nGJets_value_SigmaIetaIeta + nQCD_value_SigmaIetaIeta;

cout<<"result of fit with SigmaIetaIeta: " <<endl;
cout<<"fraction of GJets = "<<nGJets_value_SigmaIetaIeta<<" +/- "<<nGJets_value_SigmaIetaIeta_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_SigmaIetaIeta/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_SigmaIetaIeta_err/N_total_GJets_QCD_fit<<endl;
cout<<"fraction of QCD = "<<nQCD_value_SigmaIetaIeta<<" +/- "<<nQCD_value_SigmaIetaIeta_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_SigmaIetaIeta/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_SigmaIetaIeta_err/N_total_GJets_QCD_fit<<endl;

if(doAllBkgFracFit)
{
	//sigmaEOverE
	TH1F *h1_sigmaEOverE_Data = new TH1F("h1_sigmaEOverE_Data","h1_sigmaEOverE_Data", 100, 0., 0.5);
	tree_data->Draw("pho1sigmaEOverE>>h1_sigmaEOverE_Data", cut.c_str());

	TH1F *h1_sigmaEOverE_GJets = (TH1F*)file_shape->Get("phosigmaEOverE_histGJets"); 
	TH1F *h1_sigmaEOverE_QCD = (TH1F*)file_shape->Get("phosigmaEOverE_histQCD"); 

	h1_sigmaEOverE_GJets->Scale((1.0*h1_sigmaEOverE_Data->Integral())/h1_sigmaEOverE_GJets->Integral());
	h1_sigmaEOverE_QCD->Scale((1.0*h1_sigmaEOverE_Data->Integral())/h1_sigmaEOverE_QCD->Integral());

	RooWorkspace * w_frac_sigmaEOverE;
	w_frac_sigmaEOverE = FitDataBkgFraction(h1_sigmaEOverE_Data, "pho1sigmaEOverE", "#sigma_{E}/E", "", lumi, 0., 0.5, h1_sigmaEOverE_GJets, h1_sigmaEOverE_QCD);
	w_frac_sigmaEOverE->Write("w_frac_sigmaEOverE");

	float nGJets_value_sigmaEOverE = w_frac_sigmaEOverE->var("nGJets")->getValV();
	float nGJets_value_sigmaEOverE_err = w_frac_sigmaEOverE->var("nGJets")->getError();
	float nQCD_value_sigmaEOverE = w_frac_sigmaEOverE->var("nQCD")->getValV();
	float nQCD_value_sigmaEOverE_err = w_frac_sigmaEOverE->var("nQCD")->getError();
	h1_sigmaEOverE_GJets->Scale(nGJets_value_sigmaEOverE);
	h1_sigmaEOverE_QCD->Scale(nQCD_value_sigmaEOverE);
	h1_sigmaEOverE_GJets->Write();
	h1_sigmaEOverE_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_sigmaEOverE + nQCD_value_sigmaEOverE;
	cout<<"result of fit with sigmaEOverE: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_sigmaEOverE<<" +/- "<<nGJets_value_sigmaEOverE_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_sigmaEOverE/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_sigmaEOverE_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_sigmaEOverE<<" +/- "<<nQCD_value_sigmaEOverE_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_sigmaEOverE/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_sigmaEOverE_err/N_total_GJets_QCD_fit<<endl;

	//Smajor
	TH1F *h1_Smajor_Data = new TH1F("h1_Smajor_Data","h1_Smajor_Data", 100, 0., 1.0);
	tree_data->Draw("pho1Smajor>>h1_Smajor_Data", cut.c_str());

	TH1F *h1_Smajor_GJets = (TH1F*)file_shape->Get("Smajor_histGJets"); 
	TH1F *h1_Smajor_QCD = (TH1F*)file_shape->Get("Smajor_histQCD"); 

	h1_Smajor_GJets->Scale((1.0*h1_Smajor_Data->Integral())/h1_Smajor_GJets->Integral());
	h1_Smajor_QCD->Scale((1.0*h1_Smajor_Data->Integral())/h1_Smajor_QCD->Integral());

	RooWorkspace * w_frac_Smajor;
	w_frac_Smajor = FitDataBkgFraction(h1_Smajor_Data, "pho1Smajor", "S_{major}", "", lumi, 0., 1.0, h1_Smajor_GJets, h1_Smajor_QCD);
	w_frac_Smajor->Write("w_frac_Smajor");

	float nGJets_value_Smajor = w_frac_Smajor->var("nGJets")->getValV();
	float nGJets_value_Smajor_err = w_frac_Smajor->var("nGJets")->getError();
	float nQCD_value_Smajor = w_frac_Smajor->var("nQCD")->getValV();
	float nQCD_value_Smajor_err = w_frac_Smajor->var("nQCD")->getError();
	h1_Smajor_GJets->Scale(nGJets_value_Smajor);
	h1_Smajor_QCD->Scale(nQCD_value_Smajor);
	h1_Smajor_GJets->Write();
	h1_Smajor_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_Smajor + nQCD_value_Smajor;
	cout<<"result of fit with Smajor: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_Smajor<<" +/- "<<nGJets_value_Smajor_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_Smajor/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_Smajor_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_Smajor<<" +/- "<<nQCD_value_Smajor_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_Smajor/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_Smajor_err/N_total_GJets_QCD_fit<<endl;

	//nJets
	TH1F *h1_nJets_Data = new TH1F("h1_nJets_Data","h1_nJets_Data", 15,-0.5,14.5);
	tree_data->Draw("n_Jets>>h1_nJets_Data", cut.c_str());

	TH1F *h1_nJets_GJets = (TH1F*)file_shape->Get("nJets_histGJets"); 
	TH1F *h1_nJets_QCD = (TH1F*)file_shape->Get("nJets_histQCD"); 

	//TH1F *h1_nJets_GJets = new TH1F("h1_nJets_GJets","h1_nJets_GJets", 15,-0.5,14.5);
	//tree_data->Draw("n_Jets>>h1_nJets_GJets", cut_GJets.c_str());

	//TH1F *h1_nJets_QCD = new TH1F("h1_nJets_QCD","h1_nJets_QCD", 15,-0.5,14.5);
	//tree_data->Draw("n_Jets>>h1_nJets_QCD", (cut_loose + " && ! (" + cut + ")").c_str());

	h1_nJets_GJets->Scale((1.0*h1_nJets_Data->Integral())/h1_nJets_GJets->Integral());
	h1_nJets_QCD->Scale((1.0*h1_nJets_Data->Integral())/h1_nJets_QCD->Integral());

	RooWorkspace * w_frac_nJets;
	w_frac_nJets = FitDataBkgFraction(h1_nJets_Data, "nJets", "number of jets", "", lumi, -0.5, 14.5, h1_nJets_GJets, h1_nJets_QCD);
	w_frac_nJets->Write("w_frac_nJets");

	float nGJets_value_nJets = w_frac_nJets->var("nGJets")->getValV();
	float nGJets_value_nJets_err = w_frac_nJets->var("nGJets")->getError();
	float nQCD_value_nJets = w_frac_nJets->var("nQCD")->getValV();
	float nQCD_value_nJets_err = w_frac_nJets->var("nQCD")->getError();
	h1_nJets_GJets->Scale(nGJets_value_nJets);
	h1_nJets_QCD->Scale(nQCD_value_nJets);
	h1_nJets_GJets->Write();
	h1_nJets_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_nJets + nQCD_value_nJets;
	cout<<"result of fit with nJets: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_nJets<<" +/- "<<nGJets_value_nJets_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_nJets/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_nJets_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_nJets<<" +/- "<<nQCD_value_nJets_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_nJets/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_nJets_err/N_total_GJets_QCD_fit<<endl;

	//Pt
	TH1F *h1_Pt_Data = new TH1F("h1_Pt_Data","h1_Pt_Data", 100, 50., 1500);
	tree_data->Draw("pho1Pt>>h1_Pt_Data", cut.c_str());

	TH1F *h1_Pt_GJets = (TH1F*)file_shape->Get("phoPt_histGJets"); 
	TH1F *h1_Pt_QCD = (TH1F*)file_shape->Get("phoPt_histQCD"); 

	h1_Pt_GJets->Scale((1.0*h1_Pt_Data->Integral())/h1_Pt_GJets->Integral());
	h1_Pt_QCD->Scale((1.0*h1_Pt_Data->Integral())/h1_Pt_QCD->Integral());

	RooWorkspace * w_frac_Pt;
	w_frac_Pt = FitDataBkgFraction(h1_Pt_Data, "pho1Pt", "p_{T}^{#gamma}", "GeV", lumi, 50., 1500, h1_Pt_GJets, h1_Pt_QCD);
	w_frac_Pt->Write("w_frac_Pt");

	float nGJets_value_Pt = w_frac_Pt->var("nGJets")->getValV();
	float nGJets_value_Pt_err = w_frac_Pt->var("nGJets")->getError();
	float nQCD_value_Pt = w_frac_Pt->var("nQCD")->getValV();
	float nQCD_value_Pt_err = w_frac_Pt->var("nQCD")->getError();
	h1_Pt_GJets->Scale(nGJets_value_Pt);
	h1_Pt_QCD->Scale(nQCD_value_Pt);
	h1_Pt_GJets->Write();
	h1_Pt_QCD->Write();

	N_total_GJets_QCD_fit = nGJets_value_Pt + nQCD_value_Pt;
	cout<<"result of fit with Pt: " <<endl;
	cout<<"fraction of GJets = "<<nGJets_value_Pt<<" +/- "<<nGJets_value_Pt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nGJets_value_Pt/N_total_GJets_QCD_fit<<" +/- "<<nGJets_value_Pt_err/N_total_GJets_QCD_fit<<endl;
	cout<<"fraction of QCD = "<<nQCD_value_Pt<<" +/- "<<nQCD_value_Pt_err<<" / "<<N_total_GJets_QCD_fit<<" = "<<nQCD_value_Pt/N_total_GJets_QCD_fit<<" +/- "<<nQCD_value_Pt_err/N_total_GJets_QCD_fit<<endl;

}

/*
//TFractionFitter fit with SigmaIetaIeta
TH1F *h1_SigmaIetaIeta_data = new TH1F("h1_SigmaIetaIeta_data","h1_SigmaIetaIeta_data", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_data", cut.c_str());
TH1F *h1_SigmaIetaIeta_GJets = new TH1F("h1_SigmaIetaIeta_GJets","h1_SigmaIetaIeta_GJets", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_GJets", cut_GJets.c_str());
TH1F *h1_SigmaIetaIeta_QCD = new TH1F("h1_SigmaIetaIeta_QCD","h1_SigmaIetaIeta_QCD", 100, 0.005, 0.025);
tree_data->Draw("pho1SigmaIetaIeta>>h1_SigmaIetaIeta_QCD", (cut_loose + " && ! (" + cut + ")").c_str());
h1_SigmaIetaIeta_GJets->Scale(1.0*h1_SigmaIetaIeta_data->Integral()/h1_SigmaIetaIeta_GJets->Integral());
h1_SigmaIetaIeta_QCD->Scale(1.0*h1_SigmaIetaIeta_data->Integral()/h1_SigmaIetaIeta_QCD->Integral());

TFractionFitter* fit_SigmaIetaIeta;
fit_SigmaIetaIeta = FitDataBkgFractionFilter(h1_SigmaIetaIeta_data, h1_SigmaIetaIeta_GJets, h1_SigmaIetaIeta_QCD);
Double_t nGJets_value_SigmaIetaIeta, nGJets_value_SigmaIetaIeta_err, nQCD_value_SigmaIetaIeta, nQCD_value_SigmaIetaIeta_err;
fit_SigmaIetaIeta->GetResult(0, nGJets_value_SigmaIetaIeta, nGJets_value_SigmaIetaIeta_err);
fit_SigmaIetaIeta->GetResult(1, nQCD_value_SigmaIetaIeta, nQCD_value_SigmaIetaIeta_err);

cout<<"result of fit with SigmaIetaIeta: " <<endl;
cout<<"fraction of GJets = "<<nGJets_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;
cout<<"fraction of QCD = "<<nQCD_value_SigmaIetaIeta<<" / "<<nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta<<" = "<<nQCD_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta)<<endl;
*/

float frac_GJets = nGJets_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta);
float frac_QCD = nQCD_value_SigmaIetaIeta/(nGJets_value_SigmaIetaIeta+nQCD_value_SigmaIetaIeta);



/***************************Binning optimization*********************************/

float time_Low = -15.0;
float time_High = 15.0;
int time_N_fine = 300;

float met_Low = 0.0;
float met_High = 1000.0;
int met_N_fine = 200;

std::vector <int> timeBin;
std::vector <int> metBin;

timeBin.push_back(0);
timeBin.push_back(time_N_fine);

metBin.push_back(0);
metBin.push_back(met_N_fine);

if(fitMode == "binning")
{
	mkdir("fit_results/2016/binning_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/binning_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/binning_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/binning_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);

	TH2F *h2finebinData = new TH2F("h2finebinData","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinBkg = new TH2F("h2finebinBkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinGJets = new TH2F("h2finebinGJets","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinQCD = new TH2F("h2finebinQCD","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);
	TH2F *h2finebinSig = new TH2F("h2finebinSig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", time_N_fine, time_Low, time_High, met_N_fine, met_Low, met_High);

	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinData", cut.c_str());
	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinGJets", cut_GJets.c_str());
	tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinQCD", (cut_loose + " && ! (" + cut + ")").c_str());
	tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2finebinSig", (weight_cut + "( "+cut+" )").c_str());

	float N_sig_expected = 1.0*lumi*xsec*h2finebinSig->Integral()/(1.0*NEvents_sig);
	h2finebinGJets->Scale((1.0*h2finebinData->Integral()*frac_GJets)/(1.0*h2finebinGJets->Integral()));
	h2finebinQCD->Scale((1.0*h2finebinData->Integral()*frac_QCD)/(1.0*h2finebinQCD->Integral()));
	h2finebinSig->Scale((1.0*N_sig_expected)/(1.0*h2finebinSig->Integral()));

	for(int i=1; i<=time_N_fine;i++)
	{
		for(int j=1;j<=met_N_fine;j++)
		{
			h2finebinBkg->SetBinContent(i,j, h2finebinGJets->GetBinContent(i,j) + h2finebinQCD->GetBinContent(i,j));	
		}
	}

	OptimizeBinning(timeBin, metBin, h2finebinBkg, h2finebinSig, time_Low, time_High, time_N_fine, met_Low, met_High, met_N_fine, _sigModelName, outBinningDir);
	
	cout<<"optimized met and time bin:-----------"<<endl;
	cout<<"time: ";
	for(int i=0;i<timeBin.size();i++)
	{
		cout<<time_Low + (time_High - time_Low) * (1.0*timeBin[i])/(1.0*time_N_fine)<<"  ,  ";
	}
	cout<<endl;
	
	cout<<"time bin: ";
	for(int i=0;i<timeBin.size();i++)
	{
		cout<<timeBin[i]<<"  ,  ";
	}
	cout<<endl;
	
	cout<<"met: ";
	for(int i=0;i<metBin.size();i++)
	{
		cout<<met_Low + (met_High - met_Low) * (1.0*metBin[i])/(1.0*met_N_fine)<<"  ,  ";
	}
	cout<<endl;

	cout<<"met bin: ";
	for(int i=0;i<metBin.size();i++)
	{
		cout<<metBin[i]<<"   ,   ";
	}
	cout<<endl;


}

/*********2D fit of time and MET to obtain signal and background yield***********/

//2D to 1D conversion, with customize binning

TH2F * h2newbinData = new TH2F("h2newbinData","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinBkg = new TH2F("h2newbinBkg","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinGJets = new TH2F("h2newbinGJets","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinQCD = new TH2F("h2newbinQCD","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinSig = new TH2F("h2newbinSig","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinSig_JESUp = new TH2F("h2newbinSig_JESUp","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinSig_TimeCorrUp = new TH2F("h2newbinSig_TimeCorrUp","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinSig_JESDown = new TH2F("h2newbinSig_JESDown","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH2F * h2newbinSig_TimeCorrDown = new TH2F("h2newbinSig_TimeCorrDown","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT, Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);

TH1F * h1newbinData_time = new TH1F("h1newbinData_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinData_toy_time = new TH1F("h1newbinData_toy_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinBkg_time = new TH1F("h1newbinBkg_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinSig_time = new TH1F("h1newbinSig_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinEWK_time = new TH1F("h1newbinEWK_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinAll_time = new TH1F("h1newbinAll_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinGJets_time = new TH1F("h1newbinGJets_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);
TH1F * h1newbinQCD_time = new TH1F("h1newbinQCD_time","; #gamma cluster time (ns); Events", Nbins_time, useLowTBinning ? xbins_time_lowT : xbins_time_highT);


TH1F * h1newbinData_MET = new TH1F("h1newbinData_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinData_toy_MET = new TH1F("h1newbinData_toy_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinBkg_MET = new TH1F("h1newbinBkg_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinSig_MET = new TH1F("h1newbinSig_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinEWK_MET = new TH1F("h1newbinEWK_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinEWK_MET_JESUp = new TH1F("h1newbinEWK_MET_JESUp","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinEWK_MET_JESDown = new TH1F("h1newbinEWK_MET_JESDown","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinAll_MET = new TH1F("h1newbinAll_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinGJets_MET = new TH1F("h1newbinGJets_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
TH1F * h1newbinQCD_MET = new TH1F("h1newbinQCD_MET","; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);

tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2newbinData", cut.c_str());
tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2newbinGJets", cut_GJets.c_str());
tree_data->Draw("t1MET:pho1ClusterTime_SmearToData>>h2newbinQCD", (cut_loose + " && ! (" + cut + ")").c_str());
tree_signal->Draw("t1MET:pho1ClusterTime_SmearToData>>h2newbinSig", (weight_cut + "( "+cut+" )").c_str());
tree_signal->Draw("t1MET_JESUp:pho1ClusterTime_SmearToData>>h2newbinSig_JESUp", (weight_cut + "( "+cut_JESUp+" )").c_str());
tree_signal->Draw("t1MET:(pho1ClusterTime_SmearToData+0.03)>>h2newbinSig_TimeCorrUp", (weight_cut + "( "+cut+" )").c_str());
tree_signal->Draw("t1MET_JESDown:pho1ClusterTime_SmearToData>>h2newbinSig_JESDown", (weight_cut + "( "+cut_JESDown+" )").c_str());
tree_signal->Draw("t1MET:(pho1ClusterTime_SmearToData-0.03)>>h2newbinSig_TimeCorrDown", (weight_cut + "( "+cut+" )").c_str());

tree_data->Draw("pho1ClusterTime_SmearToData>>h1newbinData_time", cut.c_str());
tree_signal->Draw("pho1ClusterTime_SmearToData>>h1newbinSig_time", (weight_cut + "( "+cut+" )").c_str());
tree_data->Draw("pho1ClusterTime_SmearToData>>h1newbinGJets_time", cut_GJets.c_str());
tree_data->Draw("pho1ClusterTime_SmearToData>>h1newbinQCD_time", (cut_loose + " && ! (" + cut + ")").c_str());

tree_data->Draw("t1MET>>h1newbinData_MET", cut.c_str());
tree_signal->Draw("t1MET>>h1newbinSig_MET", (weight_cut + "( "+cut+" )").c_str());
tree_data->Draw("t1MET>>h1newbinGJets_MET", cut_GJets.c_str());
tree_data->Draw("t1MET>>h1newbinQCD_MET", (cut_loose + " && ! (" + cut + ")").c_str());

//EWK time: control region
tree_data->Draw("pho1ClusterTime_SmearToData>>h1newbinEWK_time", cut_EWKCR.c_str());
//EWK MET: from MC sample

for(int i=0; i<xsec_EWK.size(); i++)
{
	TH1F * h1newbinEWK_this_MET = new TH1F(("h1newbinEWK_this_MET_"+std::to_string(i)).c_str(),"; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
	TH1F * h1newbinEWK_this_MET_JESUp = new TH1F(("h1newbinEWK_this_MET_JESUp_"+std::to_string(i)).c_str(),"; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
	TH1F * h1newbinEWK_this_MET_JESDown = new TH1F(("h1newbinEWK_this_MET_JESDown_"+std::to_string(i)).c_str(),"; #slash{E}_{T} (GeV); Events", Nbins_MET, useLowTBinning ? xbins_MET_lowT : xbins_MET_highT);
	trees_EWK[i]->Draw(("t1MET>>h1newbinEWK_this_MET_"+std::to_string(i)).c_str(), (weight_cut + "( "+cut+" )").c_str());
	trees_EWK[i]->Draw(("t1MET_JESUp>>h1newbinEWK_this_MET_JESUp_"+std::to_string(i)).c_str(), (weight_cut + "( "+cut+" )").c_str());
	trees_EWK[i]->Draw(("t1MET_JESDown>>h1newbinEWK_this_MET_JESDown_"+std::to_string(i)).c_str(), (weight_cut + "( "+cut+" )").c_str());
	
	float int_ewk_this = h1newbinEWK_this_MET->Integral();
	properScale(h1newbinEWK_this_MET, 1.0*lumi*xsec_EWK[i]/NEvents_EWK[i]);	
	properScale(h1newbinEWK_this_MET_JESUp, 1.0*lumi*xsec_EWK[i]/NEvents_EWK[i]);	
	properScale(h1newbinEWK_this_MET_JESDown, 1.0*lumi*xsec_EWK[i]/NEvents_EWK[i]);	
	
	cout<<"total number of events in EWK background "<<i<<": before cut => after cut => scaled ... "<<trees_EWK[i]->GetEntries()<<"   "<<trees_EWK[i]->GetEntries((weight_cut + "( "+cut+" )").c_str())<<"   "<<h1newbinEWK_this_MET->Integral()<<" (  lumi*xsec*int/Norm = "<<lumi<<" * "<<xsec_EWK[i]<<" * "<<int_ewk_this<<" / "<<NEvents_EWK[i]<<" = "<<lumi*xsec_EWK[i]*int_ewk_this/NEvents_EWK[i]<<" )"<<endl;	
	h1newbinEWK_MET->Add(h1newbinEWK_this_MET);	
	h1newbinEWK_MET_JESUp->Add(h1newbinEWK_this_MET_JESUp);	
	h1newbinEWK_MET_JESDown->Add(h1newbinEWK_this_MET_JESDown);	
}


float total_norm_EWK = h1newbinEWK_MET->Integral();

h1newbinEWK_time->Scale(1.0/h1newbinEWK_time->Integral());
h1newbinEWK_MET->Scale(1.0/h1newbinEWK_MET->Integral());
h1newbinEWK_MET_JESUp->Scale(1.0/h1newbinEWK_MET_JESUp->Integral());
h1newbinEWK_MET_JESDown->Scale(1.0/h1newbinEWK_MET_JESDown->Integral());

float N_sig_expected = 1.0*lumi*xsec*h2newbinSig->Integral()/(1.0*NEvents_sig);
float N_sig_expected_JESUp = 1.0*lumi*xsec*h2newbinSig_JESUp->Integral()/(1.0*NEvents_sig);
float N_sig_expected_TimeCorrUp = 1.0*lumi*xsec*h2newbinSig_TimeCorrUp->Integral()/(1.0*NEvents_sig);
float N_sig_expected_JESDown = 1.0*lumi*xsec*h2newbinSig_JESDown->Integral()/(1.0*NEvents_sig);
float N_sig_expected_TimeCorrDown = 1.0*lumi*xsec*h2newbinSig_TimeCorrDown->Integral()/(1.0*NEvents_sig);

h2newbinGJets->Scale(((1.0*h2newbinData->Integral()-total_norm_EWK)*frac_GJets)/(1.0*h2newbinGJets->Integral()));
h2newbinQCD->Scale(((1.0*h2newbinData->Integral()-total_norm_EWK)*frac_QCD)/(1.0*h2newbinQCD->Integral()));
h2newbinSig->Scale((1.0*N_sig_expected)/(1.0*h2newbinSig->Integral()));
h2newbinSig_JESUp->Scale((1.0*N_sig_expected_JESUp)/(1.0*h2newbinSig_JESUp->Integral()));
h2newbinSig_TimeCorrUp->Scale((1.0*N_sig_expected_TimeCorrUp)/(1.0*h2newbinSig_TimeCorrUp->Integral()));
h2newbinSig_JESDown->Scale((1.0*N_sig_expected_JESDown)/(1.0*h2newbinSig_JESDown->Integral()));
h2newbinSig_TimeCorrDown->Scale((1.0*N_sig_expected_TimeCorrDown)/(1.0*h2newbinSig_TimeCorrDown->Integral()));

h1newbinGJets_time->Scale(((1.0*h1newbinData_time->Integral()-total_norm_EWK)*frac_GJets)/(1.0*h1newbinGJets_time->Integral()));
h1newbinQCD_time->Scale(((1.0*h1newbinData_time->Integral()-total_norm_EWK)*frac_QCD)/(1.0*h1newbinQCD_time->Integral()));
h1newbinSig_time->Scale((1.0*N_sig_expected)/(1.0*h1newbinSig_time->Integral()));

h1newbinGJets_MET->Scale(((1.0*h1newbinData_MET->Integral()-total_norm_EWK)*frac_GJets)/(1.0*h1newbinGJets_MET->Integral()));
h1newbinQCD_MET->Scale(((1.0*h1newbinData_MET->Integral()-total_norm_EWK)*frac_QCD)/(1.0*h1newbinQCD_MET->Integral()));
h1newbinSig_MET->Scale((1.0*N_sig_expected)/(1.0*h1newbinSig_MET->Integral()));


TH1F * h1combineData = new TH1F("h1combineData","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineData_subtractEWK = new TH1F("h1combineData_subtractEWK","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineData_toy = new TH1F("h1combineData_toy","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1 * h1combineData_toy_h1 = new TH1F("h1combineData_toy_h1","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineBkg = new TH1F("h1combineBkg","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineBkg_BkgEstimationUp = new TH1F("h1combineBkg_BkgEstimationUp","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineBkg_BkgEstimationDown = new TH1F("h1combineBkg_BkgEstimationDown","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineGJets = new TH1F("h1combineGJets","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineQCD = new TH1F("h1combineQCD","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineSig = new TH1F("h1combineSig","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineSig_JESUp = new TH1F("h1combineSig_JESUp","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineSig_TimeCorrUp = new TH1F("h1combineSig_TimeCorrUp","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineSig_JESDown = new TH1F("h1combineSig_JESDown","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineSig_TimeCorrDown = new TH1F("h1combineSig_TimeCorrDown","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineEWK = new TH1F("h1combineEWK","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineEWK_JESUp = new TH1F("h1combineEWK_JESUp","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineEWK_JESDown = new TH1F("h1combineEWK_JESDown","; bin ; Events", Nbins_total , 0, Nbins_total);
TH1F * h1combineAll = new TH1F("h1combineAll","; bin ; Events", Nbins_total , 0, Nbins_total);

for(int i=1;i<=Nbins_MET;i++)
{
	for(int j=1;j<=Nbins_time;j++)
	{
		int thisBin = (i-1)*Nbins_time+j;
		h1combineData->SetBinContent(thisBin, h2newbinData->GetBinContent(j,i));	
		h1combineGJets->SetBinContent(thisBin, h2newbinGJets->GetBinContent(j,i));	
		h1combineQCD->SetBinContent(thisBin, h2newbinQCD->GetBinContent(j,i));	
		h1combineBkg->SetBinContent(thisBin, h2newbinQCD->GetBinContent(j,i) + h2newbinGJets->GetBinContent(j,i));
		h1combineBkg_BkgEstimationUp->SetBinContent(thisBin, 0.2*h2newbinQCD->GetBinContent(j,i)/frac_QCD + 0.8*h2newbinGJets->GetBinContent(j,i)/frac_GJets);
		h1combineBkg_BkgEstimationDown->SetBinContent(thisBin, 0.8*h2newbinQCD->GetBinContent(j,i)/frac_QCD + 0.2*h2newbinGJets->GetBinContent(j,i)/frac_GJets);

		h1combineSig->SetBinContent(thisBin, h2newbinSig->GetBinContent(j,i));	
		h1combineSig_JESUp->SetBinContent(thisBin, h2newbinSig_JESUp->GetBinContent(j,i));	
		h1combineSig_TimeCorrUp->SetBinContent(thisBin, h2newbinSig_TimeCorrUp->GetBinContent(j,i));	
		h1combineSig_JESDown->SetBinContent(thisBin, h2newbinSig_JESDown->GetBinContent(j,i));	
		h1combineSig_TimeCorrDown->SetBinContent(thisBin, h2newbinSig_TimeCorrDown->GetBinContent(j,i));	

		h1combineEWK->SetBinContent(thisBin, h1newbinEWK_time->GetBinContent(j)*h1newbinEWK_MET->GetBinContent(i));
		h1combineEWK_JESUp->SetBinContent(thisBin, h1newbinEWK_time->GetBinContent(j)*h1newbinEWK_MET_JESUp->GetBinContent(i));
		h1combineEWK_JESDown->SetBinContent(thisBin, h1newbinEWK_time->GetBinContent(j)*h1newbinEWK_MET_JESDown->GetBinContent(i));

	}
}

h1combineEWK->Scale(total_norm_EWK/h1combineEWK->Integral());
h1combineEWK_JESUp->Scale(total_norm_EWK/h1combineEWK_JESUp->Integral());
h1combineEWK_JESDown->Scale(total_norm_EWK/h1combineEWK_JESDown->Integral());

for(int i=1; i<=Nbins_total; i++)
{
	//float ndata = h1combineData->GetBinContent(i);
	float nbkg = h1combineBkg->GetBinContent(i);
	float nbkg_BkgEstimationUp = h1combineBkg_BkgEstimationUp->GetBinContent(i);
	float nbkg_BkgEstimationDown = h1combineBkg_BkgEstimationDown->GetBinContent(i);
	float nsig = h1combineSig->GetBinContent(i);
	float nsig_JESUp = h1combineSig_JESUp->GetBinContent(i);
	float nsig_TimeCorrUp = h1combineSig_TimeCorrUp->GetBinContent(i);
	float nsig_JESDown = h1combineSig_JESDown->GetBinContent(i);
	float nsig_TimeCorrDown = h1combineSig_TimeCorrDown->GetBinContent(i);
	float nEWK = h1combineEWK->GetBinContent(i);
	float nEWK_JESUp = h1combineEWK_JESUp->GetBinContent(i);
	float nEWK_JESDown = h1combineEWK_JESDown->GetBinContent(i);
	if(nbkg < 1e-3 ) h1combineBkg->SetBinContent(i, 1e-3);
	if(nbkg_BkgEstimationUp < 1e-3 ) h1combineBkg_BkgEstimationUp->SetBinContent(i, 1e-3);
	if(nbkg_BkgEstimationDown < 1e-3 ) h1combineBkg_BkgEstimationDown->SetBinContent(i, 1e-3);
	if(nsig < 1e-3 ) h1combineSig->SetBinContent(i, 1e-3);
	if(nsig_JESUp < 1e-3 ) h1combineSig_JESUp->SetBinContent(i, 1e-3);
	if(nsig_TimeCorrUp < 1e-3 ) h1combineSig_TimeCorrUp->SetBinContent(i, 1e-3);
	if(nsig_JESDown < 1e-3 ) h1combineSig_JESDown->SetBinContent(i, 1e-3);
	if(nsig_TimeCorrDown < 1e-3 ) h1combineSig_TimeCorrDown->SetBinContent(i, 1e-3);
	if(nEWK < 1e-3 ) h1combineEWK->SetBinContent(i, 1e-3);
	if(nEWK_JESUp < 1e-3 ) h1combineEWK_JESUp->SetBinContent(i, 1e-3);
	if(nEWK_JESDown < 1e-3 ) h1combineEWK_JESDown->SetBinContent(i, 1e-3);
}
//generate toy data
RooWorkspace * ws_toy = GenerateToyData( h1combineData, h1combineGJets, h1combineQCD,  h1combineSig, h1combineEWK, frac_GJets, frac_QCD, 0.0);	
h1combineData_toy_h1 = ws_toy->data("data_toy")->createHistogram("bin", Nbins_total);
	
for(int i=1;i<=Nbins_total;i++)
{
	h1combineData_toy->SetBinContent(i, h1combineData_toy_h1->GetBinContent(i));
	h1combineData_subtractEWK->SetBinContent(i, h1combineData_toy_h1->GetBinContent(i)-h1combineEWK->GetBinContent(i));
}


cout<<"convert 2D to 1D (integral 2D/1D): "<<h2newbinData->Integral()<<" / "<<h1combineData->Integral()<<endl;

for(int i=1;i<=Nbins_MET;i++)
{
	float nbkg = h1newbinGJets_MET->GetBinContent(i)+h1newbinQCD_MET->GetBinContent(i);
	if(nbkg<1e-3) nbkg = 1e-3;
	h1newbinBkg_MET->SetBinContent(i, nbkg);
	
	h1newbinData_toy_MET->SetBinContent(i,0.0);
}

for(int i=1;i<=Nbins_time;i++)
{
	float nbkg = h1newbinGJets_time->GetBinContent(i)+h1newbinQCD_time->GetBinContent(i);
	if(nbkg<1e-3) nbkg = 1e-3;
	h1newbinBkg_time->SetBinContent(i, nbkg);
	
	h1newbinData_toy_time->SetBinContent(i,0.0);
}

if(fitMode == "datacard")
{
	mkdir("fit_results/2016/datacards_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/datacards_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/datacards_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/datacards_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);

	TFile *f_Out_combineWS = new TFile(("fit_results/2016/"+_outDataCardsDir+"/fit_combineWS_"+sigModelName+".root").c_str(),"recreate");

	////////////make datacard - 2D->1D fit/////////
	RooWorkspace * ws_combine;
	
	cout<<"DEBUG fit: input histogram ===="<<endl;
	cout<<"data: int = "<<h1combineData->Integral()<<endl;
	cout<<"data_toy: int = "<<h1combineData_toy->Integral()<<endl;
	cout<<"data_toy-EWK: int = "<<h1combineData_subtractEWK->Integral()<<endl;
	cout<<"GJets: int = "<<h1combineGJets->Integral()<<endl;
	cout<<"QCD: int = "<<h1combineQCD->Integral()<<endl;
	cout<<"QCD+GJets: int = "<<h1combineBkg->Integral()<<endl;
	cout<<"Sig: int = "<<h1combineSig->Integral()<<endl;
	cout<<"Sig_JESUp: int = "<<h1combineSig_JESUp->Integral()<<endl;
	cout<<"Sig_TimeCorrUp: int = "<<h1combineSig_TimeCorrUp->Integral()<<endl;
	cout<<"Sig_JESDown: int = "<<h1combineSig_JESDown->Integral()<<endl;
	cout<<"Sig_TimeCorrDown: int = "<<h1combineSig_TimeCorrDown->Integral()<<endl;
	cout<<"EWK: int = "<<h1combineEWK->Integral()<<endl;
	cout<<"EWK_JESUp: int = "<<h1combineEWK_JESUp->Integral()<<endl;
	cout<<"EWK_JESDown: int = "<<h1combineEWK_JESDown->Integral()<<endl;

	//ws_combine = Fit1DMETTimeDataBkgSig( h1combineData, h1combineGJets, h1combineQCD, h1combineSig, lumi, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, _useToy, outPlotsDir);
	//cout<<"DEBUG ======= below is the fit with QCD and GJets background only"<<endl;
	//mkdir("fit_results/2016/temp", S_IRWXU | S_IRWXG | S_IRWXO);
	//RooWorkspace * ws_combine_temp = Fit1DMETTimeDataBkgSig( h1combineData, h1combineGJets, h1combineQCD, h1combineSig, lumi, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, _useToy, "temp/");
	//cout<<"DEBUG ======= below is the fit with QCD and GJets background only, with data subtracted by EWK"<<endl;
	//mkdir("fit_results/2016/temp_subtractEWK", S_IRWXU | S_IRWXG | S_IRWXO);
	//RooWorkspace * ws_combine_temp_subtractEWK = Fit1DMETTimeDataBkgSig( h1combineData_subtractEWK, h1combineGJets, h1combineQCD, h1combineSig, lumi, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, _useToy, "temp_subtractEWK/");
	cout<<"DEBUG ======= below is the fit with QCD, GJets and EWK background"<<endl;
	mkdir("fit_results/2016/temp", S_IRWXU | S_IRWXG | S_IRWXO);
	RooWorkspace * ws_combine_temp = Fit1DMETTimeDataBkgSig( h1combineData_toy, h1combineGJets, h1combineQCD, h1combineSig, h1combineEWK, lumi, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, "temp/");

	cout<<"DEBUG ======= below is the fit with QCD and GJets background only, with data subtracted by EWK"<<endl;
	ws_combine = Fit1DMETTimeDataBkgSig( h1combineData_subtractEWK, h1combineGJets, h1combineQCD, h1combineSig, lumi, frac_GJets, frac_QCD, _sigModelName, _sigModelTitle, outPlotsDir);
	//rpQCDGJets
	//RooDataHist* rhQCDGJets = new RooDataHist("rhQCDGJets", "rhQCDGJets", RooArgSet(*ws_combine->var("bin")), h1combineBkg);
	//RooHistPdf * rpQCDGJets = new RooHistPdf("rpQCDGJets", "rpQCDGJets", RooArgSet(*ws_combine->var("bin")), *rhQCDGJets, 0);
	
	//ws_combine->import(*rpQCDGJets);
	//rpBkg
	RooDataHist* rhBkg = new RooDataHist("rhBkg", "rhBkg", RooArgSet(*ws_combine->var("bin")), h1combineBkg);
	RooHistPdf * rpBkg = new RooHistPdf("rpBkg", "rpBkg", RooArgSet(*ws_combine->var("bin")), *rhBkg, 0);
	
	ws_combine->import(*rpBkg);
	
	//BkgEstimationUp shape
	//RooDataHist* rhQCDGJets_BkgEstimationUp = new RooDataHist("rhQCDGJets_BkgEstimationUp", "rhQCDGJets_BkgEstimationUp", RooArgSet(*ws_combine->var("bin")), h1combineBkg_BkgEstimationUp);
	//RooHistPdf * rpQCDGJets_BkgEstimationUp = new RooHistPdf("rpQCDGJets_BkgEstimationUp", "rpQCDGJets_BkgEstimationUp", RooArgSet(*ws_combine->var("bin")), *rhQCDGJets_BkgEstimationUp, 0);

	//ws_combine->import(*rpQCDGJets_BkgEstimationUp);
	RooDataHist* rhBkg_BkgEstimationUp = new RooDataHist("rhBkg_BkgEstimationUp", "rhBkg_BkgEstimationUp", RooArgSet(*ws_combine->var("bin")), h1combineBkg_BkgEstimationUp);
	RooHistPdf * rpBkg_BkgEstimationUp = new RooHistPdf("rpBkg_BkgEstimationUp", "rpBkg_BkgEstimationUp", RooArgSet(*ws_combine->var("bin")), *rhBkg_BkgEstimationUp, 0);
	
	ws_combine->import(*rpBkg_BkgEstimationUp);
	
	//BkgEstimationDown shape
	//RooDataHist* rhQCDGJets_BkgEstimationDown = new RooDataHist("rhQCDGJets_BkgEstimationDown", "rhQCDGJets_BkgEstimationDown", RooArgSet(*ws_combine->var("bin")), h1combineBkg_BkgEstimationDown);
	//RooHistPdf * rpQCDGJets_BkgEstimationDown = new RooHistPdf("rpQCDGJets_BkgEstimationDown", "rpQCDGJets_BkgEstimationDown", RooArgSet(*ws_combine->var("bin")), *rhQCDGJets_BkgEstimationDown, 0);

	//ws_combine->import(*rpQCDGJets_BkgEstimationDown);
	
	RooDataHist* rhBkg_BkgEstimationDown = new RooDataHist("rhBkg_BkgEstimationDown", "rhBkg_BkgEstimationDown", RooArgSet(*ws_combine->var("bin")), h1combineBkg_BkgEstimationDown);
	RooHistPdf * rpBkg_BkgEstimationDown = new RooHistPdf("rpBkg_BkgEstimationDown", "rpBkg_BkgEstimationDown", RooArgSet(*ws_combine->var("bin")), *rhBkg_BkgEstimationDown, 0);

	ws_combine->import(*rpBkg_BkgEstimationDown);

	//JESUp shape
	RooDataHist* rhSig_JESUp = new RooDataHist("rhSig_JESUp", "rhSig_JESUp", RooArgSet(*ws_combine->var("bin")), h1combineSig_JESUp);
	RooHistPdf * rpSig_JESUp = new RooHistPdf("rpSig_JESUp", "rpSig_JESUp", RooArgSet(*ws_combine->var("bin")), *rhSig_JESUp, 0);
	//RooDataHist* rhEWK_JESUp = new RooDataHist("rhEWK_JESUp", "rhEWK_JESUp", RooArgSet(*ws_combine->var("bin")), h1combineEWK_JESUp);
	//RooHistPdf * rpEWK_JESUp = new RooHistPdf("rpEWK_JESUp", "rpEWK_JESUp", RooArgSet(*ws_combine->var("bin")), *rhEWK_JESUp, 0);
	ws_combine->import(*rpSig_JESUp);	
	//ws_combine->import(*rpEWK_JESUp);	
	//JESDown shape
	RooDataHist* rhSig_JESDown = new RooDataHist("rhSig_JESDown", "rhSig_JESUp", RooArgSet(*ws_combine->var("bin")), h1combineSig_JESDown);
	RooHistPdf * rpSig_JESDown = new RooHistPdf("rpSig_JESDown", "rpSig_JESDown", RooArgSet(*ws_combine->var("bin")), *rhSig_JESDown, 0);
	//RooDataHist* rhEWK_JESDown = new RooDataHist("rhEWK_JESDown", "rhEWK_JESUp", RooArgSet(*ws_combine->var("bin")), h1combineEWK_JESDown);
	//RooHistPdf * rpEWK_JESDown = new RooHistPdf("rpEWK_JESDown", "rpEWK_JESDown", RooArgSet(*ws_combine->var("bin")), *rhEWK_JESDown, 0);
	ws_combine->import(*rpSig_JESDown);	
	//ws_combine->import(*rpEWK_JESDown);	

	//TimeCorrUp shape
	RooDataHist* rhSig_TimeCorrUp = new RooDataHist("rhSig_TimeCorrUp", "rhSig_TimeCorrUp", RooArgSet(*ws_combine->var("bin")), h1combineSig_TimeCorrUp);
	RooHistPdf * rpSig_TimeCorrUp = new RooHistPdf("rpSig_TimeCorrUp", "rpSig_TimeCorrUp", RooArgSet(*ws_combine->var("bin")), *rhSig_TimeCorrUp, 0);
	ws_combine->import(*rpSig_TimeCorrUp);	
	//TimeCorrDown shape
	RooDataHist* rhSig_TimeCorrDown = new RooDataHist("rhSig_TimeCorrDown", "rhSig_TimeCorrUp", RooArgSet(*ws_combine->var("bin")), h1combineSig_TimeCorrDown);
	RooHistPdf * rpSig_TimeCorrDown = new RooHistPdf("rpSig_TimeCorrDown", "rpSig_TimeCorrDown", RooArgSet(*ws_combine->var("bin")), *rhSig_TimeCorrDown, 0);
	ws_combine->import(*rpSig_TimeCorrDown);	


	ws_combine->SetName("ws_combine");
	ws_combine->Write("ws_combine");
	
	//float nQCDGJets_2DFit_combine_DataBkgSig = ws_combine->var("fitModelQCDGJets_yield")->getValV();
	//float nQCDGJets_2DFit_combine_DataBkgSig_Err = ws_combine->var("fitModelQCDGJets_yield")->getError();
	//float nEWK_2DFit_combine_DataBkgSig = ws_combine->var("rpEWK_yield")->getValV();
	//float nEWK_2DFit_combine_DataBkgSig_Err = ws_combine->var("rpEWK_yield")->getError();
	float nEWK_2DFit_combine_DataBkgSig = total_norm_EWK;
	float nEWK_2DFit_combine_DataBkgSig_Err = 0.0;
	float nBkg_2DFit_combine_DataBkgSig = ws_combine->var("fitModelBkg_yield")->getValV();
	float nBkg_2DFit_combine_DataBkgSig_Err = ws_combine->var("fitModelBkg_yield")->getError();
	float nSig_2DFit_combine_DataBkgSig = ws_combine->var("rpSig_yield")->getValV();
	float nSig_2DFit_combine_DataBkgSig_Err = ws_combine->var("rpSig_yield")->getError();

	cout<<"result of 1D combined fit with bkg + sig: " <<endl;
	cout<<"N_obs in data = "<<N_obs_total<<endl;
	//cout<<"QCDGJets yield = "<<nQCDGJets_2DFit_combine_DataBkgSig<<" +/- "<<nQCDGJets_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nQCDGJets_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;
	//cout<<"EWK yield = "<<nEWK_2DFit_combine_DataBkgSig<<" +/- "<<nEWK_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nEWK_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;
	cout<<"EWK yield (fixed) = "<<nEWK_2DFit_combine_DataBkgSig<<" +/- "<<nEWK_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nEWK_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;
	cout<<"Bkg (QCD+GJets) yield = "<<nBkg_2DFit_combine_DataBkgSig<<" +/- "<<nBkg_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nBkg_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;
	cout<<"Sig yield = "<<nSig_2DFit_combine_DataBkgSig<<" +/- "<<nSig_2DFit_combine_DataBkgSig_Err<<"  (fraction: "<<nSig_2DFit_combine_DataBkgSig/N_obs_total<<" )"<<endl;

	//printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f\\\\ \n", sigModelName.c_str(), N_obs_total, nQCDGJets_2DFit_combine_DataBkgSig, nQCDGJets_2DFit_combine_DataBkgSig_Err, nEWK_2DFit_combine_DataBkgSig, nEWK_2DFit_combine_DataBkgSig_Err, nSig_2DFit_combine_DataBkgSig, nSig_2DFit_combine_DataBkgSig_Err);
	printf("%s & %d & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f & %6.2f \\pm %6.2f\\\\ \n", sigModelName.c_str(), N_obs_total, nBkg_2DFit_combine_DataBkgSig, nBkg_2DFit_combine_DataBkgSig_Err, total_norm_EWK, 0.0, nSig_2DFit_combine_DataBkgSig, nSig_2DFit_combine_DataBkgSig_Err);
	
	//datacards
	//MakeDataCard(_sigModelName, ws_combine, h1combineData->Integral(), nQCDGJets_2DFit_combine_DataBkgSig, nEWK_2DFit_combine_DataBkgSig, N_sig_expected, outDataCardsDir);
	MakeDataCard(_sigModelName, ws_combine, h1combineData_subtractEWK->Integral(), nBkg_2DFit_combine_DataBkgSig, N_sig_expected, outDataCardsDir);
	//********systematics*********//
	//lumi
	//AddSystematics_Norm(_sigModelName, 0.0, 0.0, 1.025, outDataCardsDir, "lumi", "lnN");	//https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/688.html
	AddSystematics_Norm(_sigModelName, 0.0, 1.025, outDataCardsDir, "lumi", "lnN");	//https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/688.html
	//photon efficiency
	//AddSystematics_Norm(_sigModelName, 0.0, 0.0, 1.01, outDataCardsDir, "Photon_", "lnN");
	AddSystematics_Norm(_sigModelName, 0.0, 1.01, outDataCardsDir, "Photon_", "lnN");
	//trigger efficiency
	//AddSystematics_Norm(_sigModelName, 0.0, 0.0, 1.01, outDataCardsDir, "Trigger_", "lnN");
	AddSystematics_Norm(_sigModelName, 0.0, 1.01, outDataCardsDir, "Trigger_", "lnN");
	//JES
	//AddSystematics_shape(_sigModelName, "-", "1", "1", outDataCardsDir, "JES", "shapeN2");	
	AddSystematics_shape(_sigModelName, "-", "1", outDataCardsDir, "JES", "shapeN2");
	//Timing correction
	//AddSystematics_shape(_sigModelName, "-", "-", "1", outDataCardsDir, "TimeCorr", "shapeN2");	
	AddSystematics_shape(_sigModelName, "-", "1", outDataCardsDir, "TimeCorr", "shapeN2");
	//Bkg estimation correction
	//AddSystematics_shape(_sigModelName, "1", "-", "-", outDataCardsDir, "BkgEstimation", "shapeN2");	
	AddSystematics_shape(_sigModelName, "1", "-", outDataCardsDir, "BkgEstimation", "shapeN2");
		
	h1newbinData_time->Write();
	h1newbinBkg_time->Write();
	h1newbinSig_time->Write();
	h1newbinEWK_time->Write();
	h1newbinData_MET->Write();
	h1newbinBkg_MET->Write();
	h1newbinSig_MET->Write();
	h1newbinEWK_MET->Write();
		
	h1combineData->Write();
	h1combineBkg->Write();
	h1combineSig->Write();
	h1combineEWK->Write();
	
	for(int i=1;i<=Nbins_total;i++)
	{
		int bin_time = (i-1)%Nbins_time + 1;//1->20
		int bin_MET = int((i-1)/Nbins_time) + 1; // 1->15
	
		//cout<<"DEBUG: 2Dbin = "<<i<<" time bin = "<<bin_time<<"  MET bin = "<<bin_MET<<endl;
			
		float newMET = h1newbinData_toy_MET->GetBinContent(bin_MET) + h1combineData_toy->GetBinContent(i);
		float newtime = h1newbinData_toy_time->GetBinContent(bin_time) + h1combineData_toy->GetBinContent(i);
		h1newbinData_toy_MET->SetBinContent(bin_MET,newMET);
		h1newbinData_toy_time->SetBinContent(bin_time,newtime);
	}

	
	cout<<"DEBUG: comparing real data and toy data:"<<endl;
	cout<<"toy data, 2D int = "<<h1combineData_toy->Integral()<<endl;
	cout<<"real data, MET int = "<<h1newbinData_MET->Integral()<<endl;
	cout<<"toy data, MET int = "<<h1newbinData_toy_MET->Integral()<<endl;
	cout<<"real data, time int = "<<h1newbinData_time->Integral()<<endl;
	cout<<"toy data, time int = "<<h1newbinData_toy_time->Integral()<<endl;
	
	//h1newbinBkg_time->Scale((1.0*nQCDGJets_2DFit_combine_DataBkgSig)/(1.0*h1newbinBkg_time->Integral()));
	h1newbinBkg_time->Scale((1.0*nBkg_2DFit_combine_DataBkgSig)/(1.0*h1newbinBkg_time->Integral()));
	//h1newbinBkg_MET->Scale((1.0*nQCDGJets_2DFit_combine_DataBkgSig)/(1.0*h1newbinBkg_MET->Integral()));
	h1newbinBkg_MET->Scale((1.0*nBkg_2DFit_combine_DataBkgSig)/(1.0*h1newbinBkg_MET->Integral()));
	h1newbinEWK_time->Scale((1.0*nEWK_2DFit_combine_DataBkgSig)/(1.0*h1newbinEWK_time->Integral()));
	h1newbinEWK_MET->Scale((1.0*nEWK_2DFit_combine_DataBkgSig)/(1.0*h1newbinEWK_MET->Integral()));
	h1newbinSig_time->Scale((1.0*nSig_2DFit_combine_DataBkgSig)/(1.0*h1newbinSig_time->Integral()));
	h1newbinSig_MET->Scale((1.0*nSig_2DFit_combine_DataBkgSig)/(1.0*h1newbinSig_MET->Integral()));
	
	h1combineBkg->Scale((1.0*nBkg_2DFit_combine_DataBkgSig)/(1.0*h1combineBkg->Integral()));
	h1combineSig->Scale((1.0*nSig_2DFit_combine_DataBkgSig)/(1.0*h1combineSig->Integral()));
	h1combineEWK->Scale((1.0*nEWK_2DFit_combine_DataBkgSig)/(1.0*h1combineEWK->Integral()));

	for(int i=1;i<=Nbins_MET;i++)
	{
		h1newbinAll_MET->SetBinContent(i, h1newbinBkg_MET->GetBinContent(i)+h1newbinSig_MET->GetBinContent(i)+h1newbinEWK_MET->GetBinContent(i));
	}

	for(int i=1;i<=Nbins_time;i++)
	{
		h1newbinAll_time->SetBinContent(i, h1newbinBkg_time->GetBinContent(i)+h1newbinSig_time->GetBinContent(i)+h1newbinEWK_time->GetBinContent(i));
	}
	for(int i=1;i<=Nbins_total;i++)
	{
		
		h1combineAll->SetBinContent(i, h1combineBkg->GetBinContent(i)+h1combineSig->GetBinContent(i)+h1combineEWK->GetBinContent(i));
	}

	if(_useToy)
	{	
		DrawDataBkgSig(h1newbinData_toy_time, h1newbinBkg_time, h1newbinEWK_time, h1newbinSig_time, h1newbinAll_time, lumi, sigModelTitle, sigModelName, "time", outPlotsDir);
		DrawDataBkgSig(h1newbinData_toy_MET, h1newbinBkg_MET, h1newbinEWK_MET, h1newbinSig_MET, h1newbinAll_MET, lumi, sigModelTitle, sigModelName, "MET", outPlotsDir);
		DrawDataBkgSig(h1combineData_toy, h1combineBkg, h1combineEWK, h1combineSig, h1combineAll, lumi, sigModelTitle, sigModelName, "bin", outPlotsDir);
	}
	else
	{
		DrawDataBkgSig(h1newbinData_time, h1newbinBkg_time, h1newbinEWK_time, h1newbinSig_time, h1newbinAll_time, lumi, sigModelTitle, sigModelName, "time", outPlotsDir);
		DrawDataBkgSig(h1newbinData_MET, h1newbinBkg_MET, h1newbinEWK_MET, h1newbinSig_MET, h1newbinAll_MET, lumi, sigModelTitle, sigModelName, "MET", outPlotsDir);
		DrawDataBkgSig(h1combineData, h1combineBkg, h1combineEWK, h1combineSig, h1combineAll, lumi, sigModelTitle, sigModelName, "bin", outPlotsDir);

	}

}

//do the bias test
if(fitMode == "bias")
{
	mkdir("fit_results/2016/bias_2J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/bias_2J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/bias_3J_withBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	mkdir("fit_results/2016/bias_3J_noBDT", S_IRWXU | S_IRWXG | S_IRWXO);
	

	Fit1DMETTimeBiasTest( h1combineData, h1combineBkg, h1combineSig, SoverB, nToys, _sigModelName, lumi, outBiasDir);	
		
}
return 0;
}
