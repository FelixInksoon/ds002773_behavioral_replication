# this file is used to make Pearson and Spearson correlation of 
# the target-recall benefit and competitor-intrusion reduction
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import sys

DECIMAL_PLACES = 5
FILE_NAME = 'results/statistics_result.tsv'
OUTPUT_DIR = 'results/figures'

def main():

    OUTPUT_FILE = 'results/participant_differences.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    df = pd.read_csv(FILE_NAME, sep='\t') 

    target = df['target-recall benefit'].iloc[:19]
    competitor = df['competitor-intrusion reduction'].iloc[:19]

    pearson_r, pearson_p = pearsonr(target, competitor)
    spearman_rho, spearman_p = spearmanr(target, competitor)

    print(f"Pearson: r={pearson_r:.5f}, p={pearson_p:.5f}")
    print(f"Spearman: ρ={spearman_rho:.5f}, p={spearman_p:.5f}")


    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")





if __name__ == '__main__':
    main()