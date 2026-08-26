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

def main():
    OUTPUT_FILE = 'results/robustness_checks_output_scores.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    random.seed(42)


    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    print("\nParticipant-level bootstrap analysis result:\n")

    pearson_r = pearsonr(df['target-recall benefit'].iloc[:19], df['competitor-intrusion reduction'].iloc[:19])[0]
    spearman_rho = spearmanr(df['target-recall benefit'].iloc[:19], df['competitor-intrusion reduction'].iloc[:19])[0]

    ori_target = df['target-recall benefit'].iloc[:19]
    ori_competitor = df['competitor-intrusion reduction'].iloc[:19]

    simu_pearson = []
    simu_spearman = []

    for times in range(TRIAL_TIMES):


        test_target = []
        test_competitor = []

        for i in range(N):
            k = random.randint(0, 18)
            test_target.append(df['target-recall benefit'][k])
            test_competitor.append(df['competitor-intrusion reduction'][k])

        simu_pearson.append(pearsonr(test_target,test_competitor)[0])
        simu_spearman.append(spearmanr(test_target,test_competitor)[0])

    simu_pearson.sort()
    simu_spearman.sort()

    
    print(f"Pearson correlation's 95% CI: [{simu_pearson[int(TRIAL_TIMES*0.025)]:.5f}, {simu_pearson[int(TRIAL_TIMES*0.975)]:.5f}]")
    print(f"Spearman correlation's 95% CI: [{simu_spearman[int(TRIAL_TIMES*0.025)]:.5f}, {simu_spearman[int(TRIAL_TIMES*0.975)]:.5f}]")
    print("\n")

    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")




if __name__ == "__main__":
    main()