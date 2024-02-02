from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis, TH2F
import ROOT as rt
import os, sys
from Aux import *
import numpy as np
import array

#lumi
lumi_2016 = 35922.0
lumi_2017 = 41530.0
lumi_2018ABC = 26930.0
lumi_2018D = 31947.0
lumi_run2 = lumi_2016 + lumi_2017 + lumi_2018ABC + lumi_2018D
lumi = lumi_run2
outputDir = '/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/OutputDNNrun2/'

#points
lambda_points = [100, 150, 200, 250, 300, 350, 400, 450, 500]
ctau_points = [10, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]

#input tree
tree_dir_2018 = "/home/taebh/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhotonLimit/fit_results/2018/datacards_noBDT"
plot_tag = "_v0"

drawObs=False
gROOT.SetBatch(True)

#gStyle
gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

#set printoption
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=200)

#mkdir
os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/limits")
os.system("cp draw_limits.py "+outputDir+"/limits")

#################plot settings###########################

#axis setting
axisTitleSize = 0.044
axisTitleOffset = 0.9
axisTitleSizeRatioX   = 0.18
axisLabelSizeRatioX   = 0.12
axisTitleOffsetRatioX = 0.94
axisTitleSizeRatioY   = 0.15
axisLabelSizeRatioY   = 0.108
axisTitleOffsetRatioY = 0.32

#Margin setting
leftMargin   = 0.12
rightMargin  = 0.05
topMargin    = 0.07
bottomMargin = 0.12
bottomMargin2 = 0.22

#Set the Canvas
myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )
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
myC.SetLogy(1)
myC.SetLogx(1)

N_lambda = len(lambda_points)
N_ctau = len(ctau_points)

r_exp_2d_grid_YEAR2018		 = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_YEAR2018	 = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_YEAR2018	 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_YEAR2018		 = np.zeros((N_ctau, N_lambda))

##################limit vs mass #######################3

index_ctau = -1
for ctau_this in ctau_points:
    index_ctau = index_ctau + 1

    xValue_lambda = []
    xValue_lambda_exp1sigma = []
    xValue_lambda_exp2sigma = []
    xValue_mass = []
    xValue_mass_exp1sigma = []
    xValue_mass_exp2sigma = []
    yValue_limit_this_Th = []

    limit_this_YEAR2018_exp2p5 = []
    limit_this_YEAR2018_exp16p0 = []
    limit_this_YEAR2018_exp50p0 = []
    limit_this_YEAR2018_exp84p0 = []
    limit_this_YEAR2018_exp97p5 = []
    limit_this_YEAR2018_obs = []
    
    yValue_limit_this_YEAR2018_exp = []
    yValue_limit_this_YEAR2018_obs = []
    yValue_limit_this_YEAR2018_exp1sigma = []
    yValue_limit_this_YEAR2018_exp2sigma = []

    ctau_this_str = str(ctau_this)

    index_lambda = - 1
    for lambda_this in lambda_points:
        print "limits for ctau = "+str(ctau_this)+" and lambda = "+str(lambda_this)
        index_lambda = index_lambda + 1
        limits_SF = 1.0
        if lambda_this == 100:
            limits_SF = 0.01
        if lambda_this == 150 and ctau_this == 10:
            limits_SF = 0.01

        minsize = 1000
        actualsize_YEAR2016 = 0
        actualsize_YEAR2017 = 0
        actualsize_YEAR2018 = 0

        YEAR2018file = tree_dir_2018+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm_2018.Asymptotic.mH120.root"
        if os.path.isfile(YEAR2018file):
            actualsize_YEAR2018 = os.path.getsize(YEAR2018file)
        else:
            print("{} does not exist".format(YEAR2018file))
            continue

        if (1):
            th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)
            file_limit_YEAR2018 = TFile(tree_dir_2018+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm_2018.Asymptotic.mH120.root")
            limits_YEAR2018 = []
            limitTree_YEAR2018 = file_limit_YEAR2018.Get("limit")
            for entry in limitTree_YEAR2018:
                limits_YEAR2018.append(entry.limit)
            print "combined limits for Lambda = {}, ctau = {}:".format(lambda_this, ctau_this)
            print limits_YEAR2018

            if len(limits_YEAR2018) < 6:
                print("limits_YEAR2018 = {}".format(limits_YEAR2018))
                continue

            for idx in range(len(limits_YEAR2018)):
                limits_YEAR2018[idx] = limits_YEAR2018[idx]*limits_SF

            xValue_lambda.append(lambda_this)
            xValue_mass.append(lambda_this*1.454-6.0)
            yValue_limit_this_Th.append(th_xsec_this)

            limit_this_YEAR2018_exp2p5.append(limits_YEAR2018[0]*th_xsec_this)	
            limit_this_YEAR2018_exp16p0.append(limits_YEAR2018[1]*th_xsec_this)	
            limit_this_YEAR2018_exp50p0.append(limits_YEAR2018[2]*th_xsec_this)	
            limit_this_YEAR2018_exp84p0.append(limits_YEAR2018[3]*th_xsec_this)	
            limit_this_YEAR2018_exp97p5.append(limits_YEAR2018[4]*th_xsec_this)	
            limit_this_YEAR2018_obs.append(limits_YEAR2018[5]*th_xsec_this)	

            r_exp_2d_grid_YEAR2018[index_ctau][index_lambda] = limits_YEAR2018[2]
            r_exp_p1sig_2d_grid_YEAR2018[index_ctau][index_lambda] = limits_YEAR2018[3]
            r_exp_m1sig_2d_grid_YEAR2018[index_ctau][index_lambda] = limits_YEAR2018[1]
            r_obs_2d_grid_YEAR2018[index_ctau][index_lambda] = limits_YEAR2018[5]
            
    NPoints_mass = len(xValue_mass)
    print("NPoints_mass = {} for ctau = {}".format(NPoints_mass, ctau_this))
    if (NPoints_mass < 1):
        print("Weirdo. Skip")
        sys.exit()
        continue

    for i in range(0, NPoints_mass):
        xValue_mass.append(xValue_mass[i])
        xValue_mass_exp1sigma.append(xValue_mass[i])
        xValue_mass_exp2sigma.append(xValue_mass[i])

        yValue_limit_this_YEAR2018_obs.append(limit_this_YEAR2018_obs[i])
        yValue_limit_this_YEAR2018_exp.append(limit_this_YEAR2018_exp50p0[i])
        yValue_limit_this_YEAR2018_exp1sigma.append(limit_this_YEAR2018_exp16p0[i])
        yValue_limit_this_YEAR2018_exp2sigma.append(limit_this_YEAR2018_exp2p5[i])


    for i in range(0, NPoints_mass):
        xValue_mass_exp1sigma.append(xValue_mass[NPoints_mass-i-1])
        xValue_mass_exp2sigma.append(xValue_mass[NPoints_mass-i-1])

        yValue_limit_this_YEAR2018_exp1sigma.append(limit_this_YEAR2018_exp84p0[NPoints_mass-i-1])
        yValue_limit_this_YEAR2018_exp2sigma.append(limit_this_YEAR2018_exp97p5[NPoints_mass-i-1])

    myC.SetLogy(1)
    myC.SetLogx(0)

    #YEAR2018
    graph_limit_vs_mass_YEAR2018_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_YEAR2018_obs))
    graph_limit_vs_mass_YEAR2018_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
    graph_limit_vs_mass_YEAR2018_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_YEAR2018_exp))
    graph_limit_vs_mass_YEAR2018_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_YEAR2018_exp1sigma))
    graph_limit_vs_mass_YEAR2018_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_YEAR2018_exp2sigma))

    graph_limit_vs_mass_YEAR2018_obs_limit.SetMarkerStyle(22)
    graph_limit_vs_mass_YEAR2018_obs_limit.SetMarkerSize(1.5)
    graph_limit_vs_mass_YEAR2018_obs_limit.SetLineColor(kBlack)
    graph_limit_vs_mass_YEAR2018_obs_limit.SetLineWidth(3)

    graph_limit_vs_mass_YEAR2018_Th_limit.SetMarkerStyle(22)
    graph_limit_vs_mass_YEAR2018_Th_limit.SetMarkerSize(1.5)
    graph_limit_vs_mass_YEAR2018_Th_limit.SetLineColor(kRed)
    graph_limit_vs_mass_YEAR2018_Th_limit.SetLineWidth(2)

    graph_limit_vs_mass_YEAR2018_exp_limit.SetMarkerStyle(19)
    graph_limit_vs_mass_YEAR2018_exp_limit.SetMarkerSize(1.5)
    graph_limit_vs_mass_YEAR2018_exp_limit.SetLineColor(kBlack)
    graph_limit_vs_mass_YEAR2018_exp_limit.SetLineWidth(3)
    graph_limit_vs_mass_YEAR2018_exp_limit.SetLineStyle(kDashed)

    graph_limit_vs_mass_YEAR2018_exp1sigma_limit.SetFillColor(kGreen)
    graph_limit_vs_mass_YEAR2018_exp2sigma_limit.SetFillColor(kYellow)

    graph_limit_vs_mass_YEAR2018_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
    graph_limit_vs_mass_YEAR2018_exp_limit.GetXaxis().SetLimits(100.0,600.0)
    graph_limit_vs_mass_YEAR2018_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
    graph_limit_vs_mass_YEAR2018_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
    graph_limit_vs_mass_YEAR2018_exp_limit.SetTitle("")

    graph_limit_vs_mass_YEAR2018_exp_limit.Draw("LA")

    graph_limit_vs_mass_YEAR2018_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
    graph_limit_vs_mass_YEAR2018_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
    graph_limit_vs_mass_YEAR2018_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
    graph_limit_vs_mass_YEAR2018_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

    graph_limit_vs_mass_YEAR2018_exp2sigma_limit.Draw("Fsame")
    graph_limit_vs_mass_YEAR2018_exp1sigma_limit.Draw("Fsame")
    if drawObs:
        graph_limit_vs_mass_YEAR2018_obs_limit.Draw("Lsame")
    graph_limit_vs_mass_YEAR2018_exp_limit.Draw("Lsame")
    graph_limit_vs_mass_YEAR2018_Th_limit.Draw("Lsame")

    drawCMS2(myC, 13, lumi)

    leg_limit_vs_mass_YEAR2018 = TLegend(0.25,0.62,0.9,0.89)

    leg_limit_vs_mass_YEAR2018.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
    leg_limit_vs_mass_YEAR2018.SetBorderSize(0)
    leg_limit_vs_mass_YEAR2018.SetTextSize(0.03)
    leg_limit_vs_mass_YEAR2018.SetLineColor(1)
    leg_limit_vs_mass_YEAR2018.SetLineStyle(1)
    leg_limit_vs_mass_YEAR2018.SetLineWidth(1)
    leg_limit_vs_mass_YEAR2018.SetFillColor(0)
    leg_limit_vs_mass_YEAR2018.SetFillStyle(1001)

    leg_limit_vs_mass_YEAR2018.AddEntry(graph_limit_vs_mass_YEAR2018_Th_limit, "Theoretical cross-section", "L")
    if drawObs:
        leg_limit_vs_mass_YEAR2018.AddEntry(graph_limit_vs_mass_YEAR2018_obs_limit, "Observed  95% CL upper limit", "L")
    leg_limit_vs_mass_YEAR2018.AddEntry(graph_limit_vs_mass_YEAR2018_exp_limit, "Expected  95% CL upper limit", "L")
    leg_limit_vs_mass_YEAR2018.AddEntry(graph_limit_vs_mass_YEAR2018_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
    leg_limit_vs_mass_YEAR2018.AddEntry(graph_limit_vs_mass_YEAR2018_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
    leg_limit_vs_mass_YEAR2018.Draw()

    myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_YEAR2018_ctau"+ctau_this_str+plot_tag+"_Run2Only.pdf")
    myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_YEAR2018_ctau"+ctau_this_str+plot_tag+"_Run2Only.png")
    myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_YEAR2018_ctau"+ctau_this_str+plot_tag+"_Run2Only.C")

##################exclusion region of ctau and Lambda/mass #######################

print "value of the 2D r grid (exp, YEAR2018) provided from samples: "
print r_exp_2d_grid_YEAR2018
print "value of the 2D r grid (obs, YEAR2018) provided from samples: "
print r_obs_2d_grid_YEAR2018

###linear interpolation to get the boundary points

lambda_point_boundary_exp_YEAR2018 = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_YEAR2018 = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_YEAR2018 = np.zeros(N_ctau)
lambda_point_boundary_obs_YEAR2018 = np.zeros(N_ctau)

for i in range(0, N_ctau):
    print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

    lambda_interp_YEAR2018 = []
    r_exp_interp_YEAR2018 = []
    r_exp_p1sig_interp_YEAR2018 = []
    r_exp_m1sig_interp_YEAR2018 = []
    r_obs_interp_YEAR2018 = []

    for j in range(0, N_lambda):
        if r_exp_2d_grid_YEAR2018[i][j] > 0.00000001:
            lambda_interp_YEAR2018.append(lambda_points[j]*1.0)
            r_exp_interp_YEAR2018.append(r_exp_2d_grid_YEAR2018[i][j]*1.0)
            r_exp_p1sig_interp_YEAR2018.append(r_exp_p1sig_2d_grid_YEAR2018[i][j]*1.0)
            r_exp_m1sig_interp_YEAR2018.append(r_exp_m1sig_2d_grid_YEAR2018[i][j]*1.0)
            r_obs_interp_YEAR2018.append(r_obs_2d_grid_YEAR2018[i][j]*1.0)
    graph_lambda_vs_r_exp_YEAR2018 =  TGraph(len(lambda_interp_YEAR2018), np.array(r_exp_interp_YEAR2018), np.array(lambda_interp_YEAR2018))
    graph_lambda_vs_r_exp_p1sig_YEAR2018 =  TGraph(len(lambda_interp_YEAR2018), np.array(r_exp_p1sig_interp_YEAR2018), np.array(lambda_interp_YEAR2018))
    graph_lambda_vs_r_exp_m1sig_YEAR2018 =  TGraph(len(lambda_interp_YEAR2018), np.array(r_exp_m1sig_interp_YEAR2018), np.array(lambda_interp_YEAR2018))
    lambda_point_boundary_exp_YEAR2018[i] = graph_lambda_vs_r_exp_YEAR2018.Eval(1.0)
    lambda_point_boundary_exp_p1sig_YEAR2018[i] = graph_lambda_vs_r_exp_p1sig_YEAR2018.Eval(1.0)
    lambda_point_boundary_exp_m1sig_YEAR2018[i] = graph_lambda_vs_r_exp_m1sig_YEAR2018.Eval(1.0)
    graph_lambda_vs_r_obs_YEAR2018 =  TGraph(len(lambda_interp_YEAR2018), np.array(r_obs_interp_YEAR2018), np.array(lambda_interp_YEAR2018))
    lambda_point_boundary_obs_YEAR2018[i] = graph_lambda_vs_r_obs_YEAR2018.Eval(1.0)

print "lambda points:"
print lambda_points
print "exp (YEAR2018) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_YEAR2018
print "exp p1sig (YEAR2018) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_YEAR2018
print "exp m1sig (YEAR2018) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_YEAR2018
print "obs (YEAR2018) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_YEAR2018



myC2D = TCanvas( "myC2D", "myC2D", 200, 10, 800, 800 )
myC2D.SetHighLightColor(2)
myC2D.SetFillColor(0)
myC2D.SetBorderMode(0)
myC2D.SetBorderSize(2)
myC2D.SetLeftMargin( leftMargin )
myC2D.SetRightMargin( rightMargin )
myC2D.SetTopMargin( topMargin )
myC2D.SetBottomMargin( bottomMargin2 )
myC2D.SetFrameBorderMode(0)
myC2D.SetFrameBorderMode(0)
myC2D.SetLogy(1)
myC2D.SetLogx(1)
myC2D.SetLogy(1)
myC2D.SetLogx(0)

lambda_point_boundary_exp_pm1sig_YEAR2018 = []
ctau_points_loop = []

for i in range(0,len(ctau_points)):
	ctau_points_loop.append(ctau_points[i])
	lambda_point_boundary_exp_pm1sig_YEAR2018.append(lambda_point_boundary_exp_p1sig_YEAR2018[i]*1.0)

for i in range(0, len(ctau_points)):
	ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 
	lambda_point_boundary_exp_pm1sig_YEAR2018.append(lambda_point_boundary_exp_m1sig_YEAR2018[len(ctau_points)-i-1]*1.0)

###YEAR2018 only
mass = np.array(1.454*lambda_point_boundary_exp_YEAR2018-6.0)
ctau = np.array(ctau_points_loop)
# graph_exclusion_exp_YEAR2018 = TGraph(len(lambda_point_boundary_exp_YEAR2018), np.array(1.454*lambda_point_boundary_exp_YEAR2018-6.0)[::-1], np.array(ctau_points)[::-1])
graph_exclusion_exp_YEAR2018 = TGraph(len(lambda_point_boundary_exp_YEAR2018), mass, ctau)

graph_exclusion_exp_YEAR2018.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_YEAR2018.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_YEAR2018.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_YEAR2018.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_YEAR2018.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_YEAR2018.GetXaxis().SetLimits(100.0, 750.0)
graph_exclusion_exp_YEAR2018.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_YEAR2018.GetYaxis().SetRangeUser(9.5,5.0e6)
graph_exclusion_exp_YEAR2018.SetTitle("")

graph_exclusion_exp_YEAR2018.SetLineColor(kRed + 1)
graph_exclusion_exp_YEAR2018.SetLineWidth(3)

graph_exclusion_exp_YEAR2018.Draw("alp")

#####ATLAS 8TeV
lambda_atlas_8TeV_2g = np.array([82.5 , 102.5,   140,   160,   180,   200,   220, 260,  300, 302.58, 300, 260, 220, 200 ])
t_atlas_8TeV_2g = np.array([ 121.81, 90.94, 46.63, 36.12, 27.18, 20.26, 14.59, 7.47, 2.6, 1.83, 1.31, 0.61, 0.39, 0.30 ])
ctau_atlas_8TeV_2g = t_atlas_8TeV_2g * 30.0
mass_atlas_8TeV_2g = lambda_atlas_8TeV_2g*1.454 - 6.0
graph_exclusion_atlas_8TeV_2g = TGraph(14, mass_atlas_8TeV_2g, ctau_atlas_8TeV_2g)
graph_exclusion_atlas_8TeV_2g.SetLineColor(8)
graph_exclusion_atlas_8TeV_2g.SetLineWidth(3)
graph_exclusion_atlas_8TeV_2g.SetLineStyle(5)

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")

####legend
leg_2d_exclusion_YEAR2018 = TLegend(0.35,0.64,0.92,0.91)
leg_2d_exclusion_YEAR2018.SetBorderSize(0)
leg_2d_exclusion_YEAR2018.SetTextSize(0.03)
leg_2d_exclusion_YEAR2018.SetLineColor(1)
leg_2d_exclusion_YEAR2018.SetLineStyle(1)
leg_2d_exclusion_YEAR2018.SetLineWidth(1)
leg_2d_exclusion_YEAR2018.SetFillColor(0)
leg_2d_exclusion_YEAR2018.SetFillStyle(1001)

leg_2d_exclusion_YEAR2018.AddEntry(graph_exclusion_exp_YEAR2018, "CMS Exp 13 TeV #gamma(#gamma) (2018)", "L")
leg_2d_exclusion_YEAR2018.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")

leg_2d_exclusion_YEAR2018.Draw()

drawCMS2(myC2D, 13, lumi)

#Lambda axis
f1_lambda = TF1("f1","(x+6.00)/1.454",72.902, 519.95)
A1_lambda = TGaxis(100.0, 1,750.0,1,"f1",1010)
A1_lambda.SetLabelFont(42)
A1_lambda.SetLabelSize(0.035)
A1_lambda.SetTextFont(42)
A1_lambda.SetTextSize(1.2)
A1_lambda.SetTitle("#Lambda [TeV]")
A1_lambda.SetTitleSize(0.04)
A1_lambda.SetTitleOffset(0.9)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_YEAR2018"+plot_tag+"_Run2Only.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_YEAR2018"+plot_tag+"_Run2Only.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_YEAR2018"+plot_tag+"_Run2Only.C")
