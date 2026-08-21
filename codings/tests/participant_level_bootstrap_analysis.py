# this file is used to do a participant-level bootstrap analysis

from scipy import stats
import pandas as pd
import random
import matplotlib.pyplot as plt 
import os
import sys

FILE_NAME = 'results/statistics_result.tsv'
N=19
TRIAL_TIMES= 10000

def main():
    OUTPUT_FILE = 'results/robustness_checks_output.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    random.seed(42)


    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    indicator = ['target', 'competitor', 'median_correct_response_latency']
    print("\nParticipant-level bootstrap analysis result:\n")
    for idct in indicator:

        original_diff_col = f'{idct}_diff'

        mean_diff_row = df[df['sub_id'] == 'Mean Paired Difference']
        original_mean_diff = float (mean_diff_row[original_diff_col].iloc[0])

        original_diff_list = df[original_diff_col].iloc[:19].tolist()
        simu_diff_list = []

        #print(original_diff_list)
        #print(original_diff_list[0])
        #print(original_diff_list[18])
        
        for times in range(TRIAL_TIMES):
            temp_sum = 0
            for i in range(N):
               temp_sum += float(original_diff_list[random.randint(0,18)])

            temp_sum = temp_sum / N
            simu_diff_list.append(temp_sum)

        simu_diff_list.sort()
        CI_lower_bound = simu_diff_list[int(TRIAL_TIMES*0.025)]
        CI_upper_bound = simu_diff_list[int(TRIAL_TIMES*0.975)]
        
        print(f'{idct}\'s Confidence Interval: [{CI_lower_bound}, {CI_upper_bound}]')
        print("\n")

    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")




if __name__ == "__main__":
    main()