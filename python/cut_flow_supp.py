from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
import numpy as np
import array
import math
from config_noBDT import weight_cut
from Aux import getXsecBR

#ctau_data = ['10', '50', '100', '200', '400', '600', '800', '1000', '1200', '10000']
#lambda_data = ['100', '150', '200', '250', '300', '350', '400']
ctau_data = ['10', '100', '1000', '10000']
#ctau_data = ['200']
lambda_data = ['100', '200', '300', '400']#, '450', '500']



cuts = ["(HLTDecision[81] == 1)", "pho1Pt > 70", "abs(pho1Eta)<1.4442", "pho1DNN > 0.0890", "pho1passEleVeto", "n_Jets > 2", "Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0", "n_Photons == 2"]
cuts_name = ["+ Signal trigger", "+ $\\gamma_1 \\pt>70\GeV$", "+ $\\gamma_1 |\\eta| < 1.4442$", "+ $\\gamma_1$ DNN ID", "+ $\\gamma_1$ electron veto", "+ nJets $\\geq3$", "+ \\MET filters", "+ $\\gamma_2 \\pt>40\\GeV$"]

gROOT.SetBatch(True)

tableFileName = "./cut_flow_Table_supp.txt"
f1=open(tableFileName, 'w')

for Ctau in ctau_data:
    eff_flow = np.zeros((len(lambda_data), len(cuts)))
    Eeff_flow = np.zeros((len(lambda_data), len(cuts)))


    for idx_lambda in range(len(lambda_data)):
        Lambda = lambda_data[idx_lambda]
        fileNameSig = '/storage/af/user/qnguyen/DelayedPhoton/CMSSW_10_6_12/src/DelayedPhotonID/deployment/output_bothpho_2016_new_signal/GMSB_L-{}TeV_Ctau-{}cm_13TeV-pythia8.root'.format(Lambda, Ctau)
        #fileNameSig = "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L"+Lambda+"TeV_Ctau"+Ctau+"cm_13TeV-pythia8.root"
        fileSig = TFile(fileNameSig, "READ")
        hNEventsThis_Sig = fileSig.Get("NEvents")
        treeSig = fileSig.Get("DelayedPhoton")

        xsec_Sig, exsec_Sig =  getXsecBR(Lambda, Ctau)

        N_total_Sig = hNEventsThis_Sig.GetBinContent(1)
        lumi_xs_Sig = xsec_Sig*35922.0
        N_beforePreselection_Sig =  lumi_xs_Sig

        final_cut = weight_cut + "("
        for idx in range(len(cuts)):
            if idx == 0:
                final_cut = final_cut + ""+ cuts[idx]
            else:
                final_cut = final_cut + "&& "+ cuts[idx]
            this_cut = final_cut + ")"
            print this_cut
            hist_this = TH1F("hist_"+str(idx)+Ctau+Lambda, "hist_"+str(idx), 100,0,100)
            treeSig.Draw("NPU>>hist_"+str(idx)+Ctau+Lambda, this_cut)

            N_this = lumi_xs_Sig*hist_this.Integral()/N_total_Sig
            print hist_this.Integral()

            #print str(N_this)+", "+str(N_beforePreselection_Sig)
            eff_this = 100.0*(N_this/N_beforePreselection_Sig)	
            Eeff_this  = 100.0*(N_this/N_beforePreselection_Sig*np.sqrt(1.0/hist_this.Integral() + 1.0/N_total_Sig))

            '''
            Eeff_thisint = int(pow(10,-1*int(math.log10(Eeff_this))+1)*Eeff_this)
            Eeff_thisP = Eeff_thisint *1.0/pow(10,-1*int(math.log10(Eeff_this))+1)
            eff_thisP = int(eff_this*pow(10,-1*int(math.log10(Eeff_this))+1))*1.0/pow(10,-1*int(math.log10(Eeff_this))+1)
            if Eeff_thisint < 5:
                Eeff_thisP = int(pow(10,-1*int(math.log10(Eeff_this))+2)*Eeff_this)*1.0/pow(10,-1*int(math.log10(Eeff_this))+2)
                eff_thisP = int(eff_this*pow(10,-1*int(math.log10(Eeff_this))+2))*1.0/pow(10,-1*int(math.log10(Eeff_this))+2)
            '''
            eff_flow[idx_lambda][idx] = eff_this
            Eeff_flow[idx_lambda][idx] = Eeff_this

        final_cut = final_cut + ")"

        #print "final cut ===> "+final_cut
        print Ctau
        print Lambda
        print eff_flow[idx_lambda]
        print Eeff_flow[idx_lambda]

    f1.write( "\\begin{table}[h!]\n")
    #f1.write( "\\footnotesize"
    f1.write( "\\begin{center}\n")
    f1.write( "\\caption{Event selection efficiency for GMSB SPS8 \\ctau~= \\SI{"+Ctau+"}{cm} and varying $\\Lambda$ (unit of efficiency$: \\%$; unit of $\\Lambda: \\TeV$) using the 2016 event selection flow summarized in Table \\ref{table:DelayedPhoton_event_selection}.}\n")
    f1.write( "\\label{tab:delayedphoton_cut_flow_ctau"+Ctau+"_2016}\n")
    f1.write( "\\resizebox{1.\\textwidth}{!}{\n")
    f1.write( "\\begin{tabular}{c|",)
    for idx_lambda in range(len(lambda_data)):
        f1.write( " c ",)
    f1.write( "}\n")
    f1.write( "\\hline\\hline")
    for idx_lambda in range(len(lambda_data)):
        f1.write( " & $\\Lambda="+lambda_data[idx_lambda]+"$ ",)
    f1.write( "\\\\\n")
    f1.write( "\\hline\n")
    f1.write( " - ",)
    for idx_lambda in range(len(lambda_data)):
        f1.write( " & $100.00 \\pm 0.00$ ",)
    f1.write( "\\\\\n")
    for idx in range(len(cuts)):
        f1.write( cuts_name[idx],)
        for idx_lambda in range(len(lambda_data)):
            f1.write( " & ${:.2f} \\pm {:.2f}$".format(eff_flow[idx_lambda][idx], Eeff_flow[idx_lambda][idx]))
        f1.write( "\\\\\n")
    f1.write( "\\hline\\hline\n")
    f1.write( "\\end{tabular}\n")
    f1.write( "}\n")
    f1.write( "\\end{center}\n")
    f1.write( "\\end{table}\n")
    f1.write( "\n")
