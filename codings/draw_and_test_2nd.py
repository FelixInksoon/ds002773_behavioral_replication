# this file is used to draw the paired plots comparing retrieval practice with restudy for target recall, competitor intrusions, and median correct response time.
# also this file is used to make t_paired test for the three indicators above.


import pandas as pd
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
import numpy as np

INPUT_FILE = 'results/summary_percentages.tsv'  
OUTPUT_DIR = 'results/figures'                 

def main():


    draw(INPUT_FILE, OUTPUT_DIR, 'paired_median_RT(2nd version).png', indicator='median_response_time')
    draw(INPUT_FILE, OUTPUT_DIR, 'paired_median_RT(2nd version).pdf', indicator='median_response_time')
    draw(INPUT_FILE, OUTPUT_DIR, 'target_recall(2nd version).png', indicator='target')
    draw(INPUT_FILE, OUTPUT_DIR, 'target_recall(2nd version).pdf', indicator='target')
    draw(INPUT_FILE, OUTPUT_DIR, 'competitor_intrusions(2nd version).png', indicator='competitor')
    draw(INPUT_FILE, OUTPUT_DIR, 'competitor_intrusions(2nd version).pdf', indicator='competitor')

    print("finish")


   
def draw(input_file, output_dir, output_filename, indicator):

    df = pd.read_csv(input_file, sep='\t')
    df_sub = df.iloc[:19].copy()  

    restudy_idct = df_sub[f'restudy_{indicator}']
    retprac_idct = df_sub[f'retprac_{indicator}']
    sub_ids = df_sub['sub_id']  

    x = sub_ids.values  

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, sid in enumerate(x):
        y1 = restudy_idct.iloc[i]
        y2 = retprac_idct.iloc[i]
       
        ax.plot([sid, sid], [y1, y2], color='gray', linestyle='-', alpha=0.6, linewidth=1)
        
        ax.scatter(sid, y1, color='blue', s=50, alpha=0.7, label='Restudy' if i == 0 else "")
        ax.scatter(sid, y2, color='red', s=50, alpha=0.7, label='Retrieval Practice' if i == 0 else "")

    
    ax.axhline(y=restudy_idct.mean(), color='blue', linestyle='--', alpha=0.5,
               label=f'Restudy Mean = {restudy_idct.mean():.3f}')
    ax.axhline(y=retprac_idct.mean(), color='red', linestyle='--', alpha=0.5,
               label=f'Retrieval Practice Mean = {retprac_idct.mean():.3f}')

    
    display_name = indicator.replace('_', ' ').title()

    if(display_name == 'Median Response Time'):
        display_name = 'Correct-Response Latency (Seconds)'
    elif(display_name == 'Target'):
        display_name = 'Target Recall (Proportion)'
    elif(display_name == 'Competitor'):
        display_name = 'Competitor Intrusions (Proportion)'
    


    ax.set_xlabel('Subject ID')
    ax.set_ylabel(display_name)
    ax.set_title(f'{display_name}: Restudy vs. Retrieval Practice')
    ax.legend()

    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)   
    save_path = os.path.join(output_dir, output_filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)  


def t_paired_test_with_output(list1, list2, indicator):
    t_statistic, p_value = stats.ttest_rel(list1, list2)
    print(f"Paired t-test results for {indicator}: t-statistic = {t_statistic:.5f}, p-value = {p_value:.5f}")
    with open('t_paired_test_results.txt', 'a') as f:
        f.write(f"Paired t-test results for {indicator}: t-statistic = {t_statistic:.5f}, p-value = {p_value:.5f}\n")
    return;

def statistic(restudy_list, retprac_list, indicator):
    mean1 = restudy_list.mean()
    mean2 = retprac_list.mean()
    SD1 = restudy_list.std()
    SD2 = retprac_list.std()

    cnt = 0 
    for i in range(len(restudy_list)):

        if retprac_list[i] < restudy_list[i]:
            cnt +=1

    with open('t_paired_test_results.txt', 'a') as f:
        f.write(f"Mean and SD for {indicator}:\n")
        f.write(f"Restudy: Mean = {mean1:.5f}, SD = {SD1:.5f}\n")
        f.write(f"Retprac: Mean = {mean2:.5f}, SD = {SD2:.5f}\n")
        f.write(f"Number of cases where Retrieval practice < Restudy: {cnt}\n\n")


if __name__ == "__main__":
    main()