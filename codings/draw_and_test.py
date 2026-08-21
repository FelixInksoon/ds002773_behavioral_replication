# this file is used to draw the paired plots comparing retrieval practice with restudy for target recall, competitor intrusions, and median correct response time.
# also this file is used to make t_paired test for the three indicators above.


import pandas as pd
import matplotlib.pyplot as plt
import os
import scipy.stats as stats

INPUT_FILE = 'summary_percentages.tsv'  
OUTPUT_DIR = './figures'                 

def main():


    draw(INPUT_FILE, OUTPUT_DIR, 'paired_median_RT.png', indicator='median_response_time')
    draw(INPUT_FILE, OUTPUT_DIR, 'target_recall.png', indicator='target')
    draw(INPUT_FILE, OUTPUT_DIR, 'competitor_intrusions.png', indicator='competitor')


   
def draw(input_file, output_dir, output_filename, indicator):
    df = pd.read_csv(input_file, sep='\t')
    df_sub = df.iloc[:19].copy()  

    restudy_idct = df_sub[f'restudy_{indicator}']
    retprac_idct = df_sub[f'retprac_{indicator}']
    sub_ids = df_sub['sub_id']

    t_paired_test_with_output(restudy_idct, retprac_idct, indicator)
    statistic(restudy_idct, retprac_idct, indicator)

    ### print(restudy_idct,retprac_idct,sub_ids)  # debugging

    fig, ax = plt.subplots(figsize=(8, 6))


    for i in range(len(sub_ids)):
        x_vals = [0, 1]                      # 0 for Restudy, 1 for Retprac
        y_vals = [restudy_idct.iloc[i], retprac_idct.iloc[i]]
        
        ax.plot(x_vals, y_vals, color='red', alpha=0.6, linewidth=1)
        
        ax.scatter(0, restudy_idct.iloc[i], color='blue', s=40, alpha=0.7)
        ax.scatter(1, retprac_idct.iloc[i], color='red', s=40, alpha=0.7)

    ax.axhline(y=restudy_idct.mean(), color='blue', linestyle='--', alpha=0.3, label=f'Restudy mean={restudy_idct.mean():.3f}')
    ax.axhline(y=retprac_idct.mean(), color='red', linestyle='--', alpha=0.3, label=f'Retprac mean={retprac_idct.mean():.3f}')

    ax.scatter([0]*len(restudy_idct), restudy_idct, color='blue', label='Restudy')
    ax.scatter([1]*len(retprac_idct), retprac_idct, color='red', label='Retprac')

    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Restudy', 'Retprac'])
    ax.set_ylabel(output_filename.split('.')[0].replace('_', ' ').title())
    ax.set_title(f'Paired Comparison: Restudy vs Retprac: {output_filename.split(".")[0].replace("_", " ").title()}')

    ax.legend()    
    plt.tight_layout()
    

    os.makedirs(OUTPUT_DIR, exist_ok=True)   
    save_path = os.path.join(OUTPUT_DIR, output_filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

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
        f.write(f"Number of cases where Retprac < Restudy: {cnt}\n\n")


if __name__ == "__main__":
    main()