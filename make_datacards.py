import os

for ctau in [10, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]:
    for L in [100,150,200,250,300,350,400,450,500]:
        for region in ['3J','3J1P']:
            for era in ['ABC','D']:
                executer = './FitABCD'
                data = './2018D/skim_DNN/EGamma_Run2018'+era+'.root'
                signal = './2018D/skim_DNN/GMSB_L'+str(L)+'TeV_Ctau'+str(ctau)+'cm_13TeV-pythia8.root'
                signal_name = '"L'+str(L)+'TeV_Ctau'+str(ctau)+'cm"'
                signal_title = '"signal (L'+str(L)+'-Ctau'+str(ctau)+')"'
                datacard = 'datacard'
                BDT = 'no'

                argv = ' '.join([executer, data, signal, signal_name, signal_title, region, datacard, BDT])
                # os.system(argv)
                # if era != 'D':
                    # os.system('mv fit_results/2018D/datacards_{region}_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt fit_results/2018{era}/datacards_{region}_noBDT'.format(era=era, region=region, L=L, ctau=ctau))

            os.system('combineCards.py ABC=fit_results/2018ABC/datacards_{region}_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt D=fit_results/2018D/datacards_{region}_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt > fit_results/2018/datacards_{region}_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt'.format(region=region, L=L, ctau=ctau))

        os.system('combineCards.py CAT1=fit_results/2018/datacards_3J1P_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt CAT2=fit_results/2018/datacards_3J_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt > fit_results/2018/datacards_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt'.format(L=L, ctau=ctau))

        os.system('combine fit_results/2018/datacards_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt -M Asymptotic -n L{L}TeV_Ctau{ctau}cm_2018'.format(L=L, ctau=ctau))
        os.system('mv higgsCombineL{L}TeV_Ctau{ctau}cm_2018.Asymptotic.mH120.root fit_results/2018/datacards_noBDT'.format(L=L, ctau=ctau))
