

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

FILE_NAME = 'results/statistics_result_in_runs.tsv'
OUTPUT_DIR = 'results/figures'

def main():
    draw_group_level()


def draw_group_level():
    df = pd.read_csv(FILE_NAME, sep='\t')
    
    metrics = [
        ('target', 'Target Recall', 'Proportion'),
        ('competitor', 'Competitor Intrusion', 'Proportion'),
        ('median_correct_response_latency', 'Correct Latency', 'Seconds')
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    for idx, (col_prefix, label, ylabel) in enumerate(metrics):
        ax = axes[idx]
        
        restudy_col = f'restudy_{col_prefix}'
        retrieval_col = f'retrieval_{col_prefix}'
        
        
        restudy_mean = df.groupby('run_id')[restudy_col].mean()
        restudy_sem = df.groupby('run_id')[restudy_col].sem()
        
        retrieval_mean = df.groupby('run_id')[retrieval_col].mean()
        retrieval_sem = df.groupby('run_id')[retrieval_col].sem()
        
        runs = [1, 2, 3]
        
        
        ax.errorbar(runs, restudy_mean, yerr=restudy_sem,
                    label='Restudy', color='blue', marker='o',
                    linewidth=1, capsize=2, markersize=4, capthick=1)
        
        ax.errorbar(runs, retrieval_mean, yerr=retrieval_sem,
                    label='Retrieval Practice', color='red', marker='s',
                    linewidth=1, capsize=2, markersize=4, capthick=1)
        
        ax.set_xlabel('Run', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(label, fontsize=16, fontweight='bold')
        ax.set_xticks(runs)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.4)
        
        
        all_vals = pd.concat([df[restudy_col], df[retrieval_col]]).dropna()
        y_min, y_max = all_vals.min(), all_vals.max()
        margin = (y_max - y_min) * 0.15
        ax.set_ylim(y_min - margin, y_max + margin)
    
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'group_level_combined(run_level).pdf'), format='pdf')
    plt.savefig(os.path.join(OUTPUT_DIR, 'group_level_combined(run_level).png'), dpi=300)
    plt.close()
    print("finish")





if __name__ == '__main__':
    main()