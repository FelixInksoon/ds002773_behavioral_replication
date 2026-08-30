# this file is used to do the paired permutation test for two scores:
# target-recall benefit', 'competitor-intrusion reduction'

from scipy import stats
import pandas as pd
import random
import sys
import numpy as np
from scipy.stats import pearsonr, spearmanr

FILE_NAME = 'results/statistics_result.tsv'
OUTPUT_FILE = 'results/composition_correlation_with_robustness_result.txt'
TRIAL_TIMES = 10000
N=19

def main():
    
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    random.seed(42)

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    print("\nPaired Permutation Test Result:\n")

    correlation_permutation('target-recall benefit', 'competitor-intrusion reduction', df)
    correlation_permutation('target-recall benefit', 'other reduction', df)
    correlation_permutation('target-recall benefit', 'don\'t know reduction', df)
    correlation_permutation('target-recall benefit', 'no response reduction', df)

    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")



def correlation_permutation(var1, var2, df):


    print(f'for {var1} and {var2}: ')


    pearson_r = pearsonr(df[f'{var1}'].iloc[:19], df[f'{var2}'].iloc[:19])[0]
    spearman_rho = spearmanr(df[f'{var1}'].iloc[:19], df[f'{var2}'].iloc[:19])[0]

    abs_ori_pearson_r = abs(pearson_r)
    abs_ori_spearman_rho = abs(spearman_rho)

    cnt_pearson = 0
    cnt_spearman = 0

    for i in range(TRIAL_TIMES):

        test1 = df[f'{var1}'].iloc[:19]
        test2 = df[f'{var2}'].iloc[:19]

        new2 = np.random.permutation(test2)

        new_pearson_r = pearsonr(test1, new2)[0]
        new_spearman_rho = spearmanr(test1, new2)[0]

        if abs(new_pearson_r) >= abs_ori_pearson_r:
            cnt_pearson += 1
        if abs(new_spearman_rho) >= abs_ori_spearman_rho:
            cnt_spearman += 1


    pearson_p = cnt_pearson / TRIAL_TIMES
    spearman_p = cnt_spearman / TRIAL_TIMES

    print(f'pearson p value: {pearson_p}\n')
    print(f'spearman p value: {spearman_p}\n')
    print("\n")


    

if __name__ == "__main__":
    main()