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
import seaborn
from matplotlib.patches import Patch

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
    # plt.scatter(benefit, reduction, color='blue', s=60, alpha=0.8, edgecolors='black', linewidth=0.5)

    slope, intercept = np.polyfit(benefit, reduction, 1)
    pearson_r, pearson_p = stats.pearsonr(benefit, reduction)
    spearman_rho, spearman_p = stats.spearmanr(benefit, reduction)

    '''x_fit = np.linspace(benefit.min(), benefit.max(), 100)
    y_fit = slope * x_fit + intercept

    
    plt.plot(x_fit, y_fit, color='red', linestyle='-', linewidth=2, label=f'Regression line')'''

    
    text_str = (
        f'Pearson r = {pearson_r:.3f}, p = {pearson_p:.4f}\n'
        f'Spearman ρ = {spearman_rho:.3f}, p = {spearman_p:.4f}'
    )

    ax = seaborn.regplot(x=benefit, y=reduction, 
                         ci=95,                
                         scatter_kws={'color': '#468BCA', 's': 60, 'alpha': 0.8},
                         line_kws={'color': '#468BCA', 'linestyle': '-', 'linewidth': 2},
                         scatter=True)

    '''
    ci_fill = ax.collections[-1] 
    print(ci_fill.get_facecolor())'''

    scatter = ax.collections[0]
    line = ax.lines[0]
    scatter.set_label('Participants')
    line.set_label('Regression Line')

    ci_patch = Patch(facecolor='#468BCA', alpha=0.25, label='95% Confidence I')

    ax.legend(handles=[scatter, line, ci_patch], loc='upper left', frameon=True, fontsize=10)
    ###plt.legend( loc='upper left',  frameon=True, fontsize=10)

    plt.text(0.025, 0.875, text_str, transform=plt.gca().transAxes,
             fontsize=13, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    for i, (xi, yi, sid) in enumerate(zip(benefit, reduction, sub_ids)):
        plt.text(xi + 0.003, yi + 0.003, str(sid), fontsize=8, ha='left', va='bottom')

    
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
    plt.savefig(os.path.join(figures_dir, 'scatter_target_benefit_vs_competitor_reduction.png'), dpi=300)
    plt.savefig(os.path.join(figures_dir, 'scatter_target_benefit_vs_competitor_reduction.pdf'), dpi=300)
    plt.close()  

    print("finish")




if __name__ == '__main__':
    main()