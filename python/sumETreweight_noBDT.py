import ROOT as root
import os, sys
import numpy as np
import array
import random
from config_noBDT import fileNameSigSkim
from config_noBDT import fileNameGJetsSkim
from config_noBDT import fileNameQCDSkim
from config_noBDT import fileNameDataSkim
from config_noBDT import fileNameData
from Aux import *

from config_noBDT import fileNameGJets, cut, cut_noDisc, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD, weight_cut
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, cut_GJets, cut_loose, xbins_MET, xbins_time, sigLegend

root.gROOT.ProcessLine("struct MyStruct{float weight_sumET;};")
from ROOT import MyStruct

random.seed(920728)



root.gROOT.SetBatch(True)

root.gStyle.SetOptStat(0)
root.gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/stack")
os.system("mkdir -p "+outputDir+"/stack")
os.system("cp config_noBDT.py "+outputDir+"/stack")
os.system("cp sumETreweight_noBDT.py "+outputDir+"/stack")
#os.system("mkdir -p ../data")
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

def GetKeyNames( self, dir = "" ):
        self.cd(dir)
        return [key.GetName() for key in root.gDirectory.GetListOfKeys()]
def GetClassNames( self, dir = "" ):
        self.cd(dir)
        return [key.GetClassName() for key in root.gDirectory.GetListOfKeys()]

root.TFile.GetKeyNames = GetKeyNames
root.TFile.GetClassNames = GetClassNames

def smear_and_fill(oldTree, newTree, s, histWeight):
	num_entries = oldTree.GetEntries()
    	for i in range(num_entries):
        	oldTree.GetEntry(i)
        	if i % 10000 == 0:
            		print "Processing event {} of {}".format(i, num_entries)
		binIndex = histWeight.FindBin(oldTree.sumMET)
		if binIndex > -1:	
			s.weight_sumET = histWeight.GetBinContent(binIndex)
		else:
			s.weight_sumET = 1.0
        	newTree.Fill()

def smear_file(inFileName, histWeight):
	#inFileName = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/skim/DelayedPhoton_DoubleEG_2016B_ver1.root"
	print "reweighting input file: "+inFileName
	inFile = root.TFile(inFileName.replace('GoodLumi','GoodLumi_noreweight'), "READ")
	inTree = inFile.Get("DelayedPhoton")

	outFile = root.TFile(inFileName, 'RECREATE')
	outTree = inTree.CloneTree(0)

	s = MyStruct()
	new_time_branch = outTree.Branch('weight_sumET',root.AddressOf(s, 'weight_sumET'), 'weight_sumET/F')

	print "Writing new ROOT file with added sumET weight"

	smear_and_fill(inTree, outTree, s, histWeight)
	outFile.cd()
	outTree.GetCurrentFile().Write()

	##copy histograms
	keyList = inFile.GetKeyNames()
        classList = inFile.GetClassNames()
	for j in range(0, len(keyList)):
                print classList[j] + "   ===   " + keyList[j]
                if classList[j] == "TH1F":
                        inFile.cd()
                        histThis = inFile.Get(keyList[j])
                        outFile.cd()
                        histThis_out = histThis.Clone()
                        histThis_out.Write()

	outTree.GetCurrentFile().Close()

xbins_sumET = [0.0, 100.0, 200.0, 400.0, 600.0, 800, 1000.0, 1250.0, 1500.0, 1750.0, 2000.0, 2500.0, 3000.0, 5000.0, 10000.0]

weightedcut_CR =  weight_cut + cut_GJets
weightedcut_SR =  weight_cut + cut

print "weightedcut_CR ===> "+ weightedcut_CR
print "weightedcut_SR ===> "+ weightedcut_SR

#######obtain the weight: SR/CR:

hist_CR = root.TH1F("hist_CR","hist_CR", len(xbins_sumET)-1, np.array(xbins_sumET))
hist_SR = root.TH1F("hist_SR","hist_SR", len(xbins_sumET)-1, np.array(xbins_sumET))
#hist_data = root.TH1F("hist_data","hist_data", len(xbins_sumET)-1, np.array(xbins_sumET))
hist_weight = root.TH1F("hist_weight","hist_weight", len(xbins_sumET)-1, np.array(xbins_sumET))

for i in range(0,len(fileNameGJets)):
	thisFile = root.TFile(fileNameGJets[i], 'READ')
	thisTree = thisFile.Get("DelayedPhoton")
	thisNEvents_hist = thisFile.Get("NEvents")
	thisNEvents = thisNEvents_hist.GetBinContent(1)

	hist_CR_this = root.TH1F("hist_CR_this_"+str(i),"hist_CR_this_"+str(i), len(xbins_sumET)-1, np.array(xbins_sumET))
	hist_SR_this = root.TH1F("hist_SR_this_"+str(i),"hist_SR_this_"+str(i), len(xbins_sumET)-1, np.array(xbins_sumET))
	
	thisTree.Draw("sumMET>>hist_CR_this_"+str(i), weightedcut_CR)	
	thisTree.Draw("sumMET>>hist_SR_this_"+str(i), weightedcut_SR)	
	
	if hist_SR_this.Integral() > 10.0:
		hist_SR_this.Scale(lumi*kFactor*xsecGJets[i]/thisNEvents)
	if hist_CR_this.Integral() > 10.0:
		hist_CR_this.Scale(lumi*kFactor*xsecGJets[i]/thisNEvents)
	
	hist_CR.Add(hist_CR_this)	
	hist_SR.Add(hist_SR_this)	

'''
fileData = root.TFile(fileNameData, 'READ')
treeData = fileData.Get("DelayedPhoton")
print "treeData.GetEntries(cut)"
print treeData.GetEntries(cut)
treeData.Draw("sumMET>>hist_data",cut)


hist_data.SetMarkerStyle( 20 )
hist_data.SetMarkerColor( 1 )
hist_data.SetLineColor( 1 )
'''


myC = root.TCanvas( "myC", "myC", 200, 10, 800, 800 )
myC.SetHighLightColor(2)
myC.SetFillColor(0)
myC.SetBorderMode(0)
myC.SetBorderSize(2)
myC.SetLeftMargin( leftMargin )
myC.SetRightMargin( rightMargin )
myC.SetTopMargin( topMargin )
myC.SetBottomMargin( bottomMargin )
myC.SetFrameBorderMode(0)
myC.SetFrameBorderMode(0)

pad1 = root.TPad("pad1","pad1", 0.05, 0.3,0.95, 0.97)
pad1.SetBottomMargin(0)
pad1.SetRightMargin( rightMargin )
pad1.SetLeftMargin( leftMargin )
pad1.SetLogy(1)
pad1.Draw()

pad2 = root.TPad("pad2","pad2", 0.05, 0.02, 0.95, 0.29)
pad2.SetTopMargin(0.04)
pad2.SetTopMargin(0.008)
pad2.SetBottomMargin(0.4)
pad2.SetRightMargin( rightMargin )
pad2.SetLeftMargin( leftMargin )
pad2.SetGridy()
pad2.Draw()

pad1.cd()

hist_CR.Scale(hist_SR.Integral()/hist_CR.Integral())
hist_CR.SetLineColor( 2 )
hist_CR.SetLineWidth( 2 )
hist_SR.SetLineColor( 4 )
hist_SR.SetLineWidth( 2 )

leg = root.TLegend(0.55, 0.7, 0.88, 0.89)
leg.SetBorderSize(0)
leg.SetTextSize(0.04)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)
#leg.AddEntry(hist_data, "SR in data", "lep")
leg.AddEntry(hist_CR, "#gamma+jets CR in #gamma+jets MC", "l")
leg.AddEntry(hist_SR, "SR in #gamma+jets MC", "l")


hist_CR.SetTitle("")
hist_CR.Draw("hist")
hist_CR.GetXaxis().SetTitleSize( axisTitleSize )
hist_CR.GetXaxis().SetTitleOffset( axisTitleOffset )
hist_CR.GetYaxis().SetTitleSize( axisTitleSize )
hist_CR.GetYaxis().SetTitleOffset( axisTitleOffset )
hist_CR.GetYaxis().SetTitle("Events")
hist_CR.SetMaximum(200.0*max(hist_CR.GetMaximum(), hist_SR.GetMaximum()))#, hist_data.GetMaximum()))

pad1.Update()
hist_SR.Draw("samehist")
#hist_data.Draw("sameE")
leg.Draw()


pad2.cd()
hist_weight.Add(hist_SR)
hist_weight.Divide(hist_CR)

hist_weight.SetMarkerStyle( 20 )
hist_weight.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
hist_weight.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
hist_weight.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
hist_weight.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
hist_weight.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
hist_weight.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
hist_weight.SetMarkerColor( 4 )
hist_weight.SetLineColor( 4 )
hist_weight.GetYaxis().SetRangeUser( 0.0, 2.5 )
hist_weight.SetTitle("")
hist_weight.GetYaxis().SetTitle("SR / CR")
hist_weight.GetYaxis().CenterTitle( True )
hist_weight.GetYaxis().SetNdivisions( 5, False )
hist_weight.SetStats( 0 )
hist_weight.Draw("E")
hist_weight.GetXaxis().SetTitle("#Sigma E_{T} [GeV]")
pad1.Update()
pad2.Update()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/stack/sumMET_CR_and_SR_in_GJetsMC.pdf")
myC.SaveAs(outputDir+"/stack/sumMET_CR_and_SR_in_GJetsMC.png")
myC.SaveAs(outputDir+"/stack/sumMET_CR_and_SR_in_GJetsMC.C")


###now do the smear
#smear_file(fileNameData, hist_weight)
smear_file(fileNameData.replace("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT","/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT"), hist_weight)
