# this file is used to calculate the target-recall benefit and competitor-intrusion reduction
# target-recall benefit = retrieval - restudy
# competitor-intrusiion reduction = restudy - retrieval
# also, it will output scatterplots showing these two variables

import csv
import statistics
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

FILE_NAME = 'results/statistics_result.tsv'
N=19

def main():

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    # print(df)

    ### target-recall benefit
    df["target-recall benefit"] = df["retprac_target"]-df["restudy_target"]
    ### competitor-intrusion reduction
    df["competitor-intrusion reduction"] = df["restudy_competitor"]-df["retprac_competitor"]
    df.to_csv(FILE_NAME, sep='\t', index=False)


    ### scatterplot
    participants = df.iloc[:19].copy()
    benefit = participants["target-recall benefit"]
    reduction = participants["competitor-intrusion reduction"]
    sub_ids = participants["sub_id"].astype(int)  
    
    plt.figure(figsize=(8, 8))
    plt.scatter(benefit, reduction, color='blue', s=60, alpha=0.8, edgecolors='black', linewidth=0.5)

    
    for i, (xi, yi, sid) in enumerate(zip(benefit, reduction, sub_ids)):
        plt.text(xi + 0.005, yi + 0.005, str(sid), fontsize=8, ha='left', va='bottom')

    
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)

    
    plt.xlabel('Target Recall Benefit (Retrieval - Restudy)', fontsize=12)
    plt.ylabel('Competitor Intrusion Reduction (Restudy - Retrieval)', fontsize=12)
    plt.title('Scatterplot: Target Benefit vs. Competitor Reduction', fontsize=16)


    plt.grid(alpha=0.2, linestyle=':')
    plt.tight_layout()

    script_dir = os.path.dirname(os.path.abspath(FILE_NAME))
    figures_dir = os.path.join(script_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    save_path = os.path.join(figures_dir, 'scatter_target_benefit_vs_competitor_reduction.png')
    plt.savefig(save_path, dpi=300)
    plt.close()  




if __name__ == '__main__':
    main()