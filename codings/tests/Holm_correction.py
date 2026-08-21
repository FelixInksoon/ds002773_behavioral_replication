# this file is used to do the Holm correction
from scipy import stats
import pandas as pd
import random
import matplotlib.pyplot as plt 
import os
import sys

FILE_NAME = 'results/statistics_result.tsv'
N=19
P_VALUE_NUM = 3


def main():
    OUTPUT_FILE = 'results/robustness_checks_output.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    indicator = ['target', 'competitor', 'median_correct_response_latency']
    significance_level = [0.05, 0.01]

    raw_p_value_row = df[df['sub_id'] == 'p value']

    origin_p = []
    p_value = []
    
    for idct in indicator:
        col_index = f'{idct}_diff'
        p_value = float(raw_p_value_row[col_index].iloc[0])
        origin_p.append((p_value, idct))

    origin_p.sort(key=lambda x:x[0])
    # print(origin_p[0])
    print("\nHolm correction's result:\n")

    

    for alpha in significance_level:
        cond = []
        adj_alpha = []

        for i in range(P_VALUE_NUM):
            adj_alpha.append(alpha / (P_VALUE_NUM -i))
            if origin_p[i][0] <= alpha / (P_VALUE_NUM -i):
                cond.append('Reject')
            else:
                cond.append('No Reject')

        print(f'For significance level {alpha}:')
        print(f'The original p values are: {origin_p}')
        print(f'The adjusted significance levels are: {adj_alpha}')
        print(f'The test results are: {cond}')
        print("\n")

    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")


    


if __name__ == "__main__":
    main()