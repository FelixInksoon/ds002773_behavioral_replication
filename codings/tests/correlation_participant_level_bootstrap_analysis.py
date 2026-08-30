# this file is used to do a participant-level bootstrap analysis for two scores: 
# target-recall benefit', 'competitor-intrusion reduction'

from scipy import stats
import pandas as pd
import random
import matplotlib.pyplot as plt 
import os
import sys
from scipy.stats import pearsonr, spearmanr
import random

FILE_NAME = 'results/statistics_result.tsv'
N=19
TRIAL_TIMES= 10000
OUTPUT_FILE = 'results/composition_correlation_with_robustness_result.txt'

def main():
    
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    random.seed(42)


    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    print("\nParticipant-level bootstrap analysis result:\n")

    correlation_bootstrap('target-recall benefit', 'competitor-intrusion reduction', df)
    correlation_bootstrap('target-recall benefit', 'other reduction', df)
    correlation_bootstrap('target-recall benefit', 'don\'t know reduction', df)
    correlation_bootstrap('target-recall benefit', 'no response reduction', df)


    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")

def correlation_bootstrap(var1, var2, df):


    print(f'for {var1} and {var2}: ')

    simu_pearson = []
    simu_spearman = []

    random.seed(42)

    for times in range(TRIAL_TIMES):


        test1 = []
        test2 = []

        for i in range(N):
            k = random.randint(0, 18)
            test1.append(df[f'{var1}'][k])
            test2.append(df[f'{var2}'][k])

        simu_pearson.append(pearsonr(test1,test2)[0])
        simu_spearman.append(spearmanr(test1,test2)[0])

    simu_pearson.sort()
    simu_spearman.sort()

    
    print(f"Pearson correlation's 95% CI: [{simu_pearson[int(TRIAL_TIMES*0.025)]:.5f}, {simu_pearson[int(TRIAL_TIMES*0.975)]:.5f}]")
    print(f"Spearman correlation's 95% CI: [{simu_spearman[int(TRIAL_TIMES*0.025)]:.5f}, {simu_spearman[int(TRIAL_TIMES*0.975)]:.5f}]")
    print("\n")




if __name__ == "__main__":
    main()