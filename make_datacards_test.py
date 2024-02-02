import os
from multiprocessing import Pool

def process_task(args):
    executer, data, signal, signal_name, signal_title, region, datacard, BDT = args
    argv = ' '.join([executer, data, signal, signal_name, signal_title, region, datacard, BDT])
    os.system(argv)
    # if era != 'D':
        # os.system('mv fit_results/2018D/datacards_{region}_noBDT/DelayedPhotonCard_L{L}TeV_Ctau{ctau}cm.txt fit_results/2018{era}/datacards_{region}_noBDT'.format(era=era, region=region, L=L, ctau=ctau))

if __name__ == "__main__":
    tasks = []

    for ctau in [10, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]:
        for L in [100, 150, 200, 250, 300, 350, 400, 450, 500]:
            for region in ['3J', '3J1P']:
                for era in ['D']:
                    executer = './FitABCD'
                    data = './2018D/skim_DNN/EGamma_Run2018' + era + '.root'
                    signal = './2018D/skim_DNN/GMSB_L' + str(L) + 'TeV_Ctau' + str(ctau) + 'cm_13TeV-pythia8.root'
                    signal_name = '"L' + str(L) + 'TeV_Ctau' + str(ctau) + 'cm"'
                    signal_title = '"signal (L' + str(L) + '-Ctau' + str(ctau) + ')"'
                    datacard = 'datacard'
                    BDT = 'no'

                    tasks.append((executer, data, signal, signal_name, signal_title, region, datacard, BDT))

    # Set the number of processes based on your system's capabilities
    num_processes = 10  # Adjust to match the number of available CPUs
    from contextlib import closing
    with closing(Pool(num_processes)) as pool:
        pool.map(process_task, tasks)
