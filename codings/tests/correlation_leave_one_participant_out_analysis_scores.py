# this file is used to do the leave-one-participant-out analysis for two scores:
# target-recall benefit', 'competitor-intrusion reduction' 
from scipy.stats import pearsonr, spearmanr
import pandas as pd
import sys

FILE_NAME = 'results/statistics_result.tsv'
OUTPUT_FILE = 'results/composition_correlation_with_robustness_result.txt'
N = 19

def main():
    
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    print("\nLeave-one-participant out (LOPO) Test Result for correlation:\n")

    LOPO_correlation('target-recall benefit', 'competitor-intrusion reduction', df)
    LOPO_correlation('target-recall benefit', 'other reduction', df)
    LOPO_correlation('target-recall benefit', 'don\'t know reduction', df)
    LOPO_correlation('target-recall benefit', 'no response reduction', df)

    sys.stdout = sys.__stdout__
    log_file.close()
    print("finish")


def LOPO_correlation(var1, var2, df):


    print(f'for {var1} and {var2}: ')
    list1 = df[f'{var1}'].iloc[:19]
    list2 = df[f'{var2}'].iloc[:19]


    print(f'original Pearson\'s r: {pearsonr(list1, list2)[0]} ,p: {pearsonr(list1, list2)[1]}')
    print(f'original Spearman\'s rho: {spearmanr(list1, list2)[0]} ,p: {spearmanr(list1, list2)[1]}')

    original_pearson = pearsonr(list1, list2)[0]
    original_spearman = spearmanr(list1, list2)[0]

    simu_pearson = []
    simu_spearman = []

    for ignore in range(N):

        test_target = list1.drop(index=ignore)
        test_competitor = list2.drop(index=ignore)
        simu_pearson.append(pearsonr(test_target, test_competitor)[0])
        simu_spearman.append(spearmanr(test_target, test_competitor)[0])


    min_val = min(simu_pearson)
    max_val = max(simu_pearson)
    std_val = pd.Series(simu_pearson).std()
    mean_val = pd.Series(simu_pearson).mean()
    print(f"\nFor Pearson correlation:")
    print(f"Original r (full sample): {original_pearson:.5f}")
    print(f"LOPO estimated r (average across 19 leave-outs): {mean_val:.5f}")
    print(f"Range of LOPO estimates: [{min_val:.5f}, {max_val:.5f}]")
    print(f"Standard deviation of LOPO estimates: {std_val:.5f}")
    sign = "positive" if min_val > 0 else "negative" if max_val < 0 else "mixed in sign"
    print(f"Conclusion: All {N} estimates remained {sign} relative to the original effect.")


    min_val = min(simu_spearman)
    max_val = max(simu_spearman)
    std_val = pd.Series(simu_spearman).std()
    mean_val = pd.Series(simu_spearman).mean()
    print(f"\nFor Spearman correlation:")
    print(f"Original r (full sample): {original_spearman:.5f}")
    print(f"LOPO estimated r (average across 19 leave-outs): {mean_val:.5f}")
    print(f"Range of LOPO estimates: [{min_val:.5f}, {max_val:.5f}]")
    print(f"Standard deviation of LOPO estimates: {std_val:.5f}")
    sign = "positive" if min_val > 0 else "negative" if max_val < 0 else "mixed in sign"
    print(f"Conclusion: All {N} estimates remained {sign} relative to the original effect.")


if __name__ == "__main__":
    main()