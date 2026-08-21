# this file is used to do the Wilcoxon signed rank test.

from scipy import stats
import pandas as pd
import sys
FILE_NAME = 'results/statistics_result.tsv'


def main():
    OUTPUT_FILE = 'results/robustness_checks_output.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file


    df = pd.read_csv(FILE_NAME, sep='\t')
    # print(df)
    pro_df = df.iloc[:19]

    indicator = ['target', 'competitor', 'median_correct_response_latency']

    print("\nWilcoxon signed rank rest result:\n")

    for idct in indicator:
        restudy_col = f'restudy_{idct}'
        retprac_col = f'retprac_{idct}'
        statistic, p_val = stats.wilcoxon(pro_df[restudy_col], pro_df[retprac_col], alternative='two-sided')

        print(f'{idct}:')
        print("Statistic: ", statistic, ", P value: ", p_val)
        print("\n")
        

    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")
    

if __name__ == "__main__":
    main()