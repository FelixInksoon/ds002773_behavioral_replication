# this file is used to do the paired permutation test

from scipy import stats
import pandas as pd
import random
import sys

FILE_NAME = 'results/statistics_result.tsv'

TRIAL_TIMES = 1000000
N=19

def main():
    OUTPUT_FILE = 'results/robustness_checks_output.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    random.seed(42)

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    indicator = ['target', 'competitor', 'median_correct_response_latency']

    print("\nPaired Permutation Test Result:\n")

    for idct in indicator:

        original_diff_col = f'{idct}_diff'

        mean_diff_row = df[df['sub_id'] == 'Mean Paired Difference']
        original_mean_diff = float (mean_diff_row[original_diff_col].iloc[0])

        original_diff_list = df[original_diff_col].iloc[:19].tolist()
        simu_mean_diff = []

        for i in range(TRIAL_TIMES):
            sum = 0
            for value in original_diff_list:
                if random.randint(1,2) == 1:
                    sum += float (value)
                else: 
                    sum -= float (value)
            simu_mean_diff.append(sum/N)

        cnt = 0
        abs_original_mean_diff = abs(original_mean_diff)

        for x in simu_mean_diff:
            if abs(x) >= abs_original_mean_diff:
                cnt +=1

        p_value = cnt / TRIAL_TIMES

        print(f'{idct}\'s p value: {p_value}')
        print("\n")

    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")






    

if __name__ == "__main__":
    main()