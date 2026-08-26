# this file is used to do the leave-one-participant-out analysis
from scipy import stats
import pandas as pd
import random
import matplotlib.pyplot as plt 
import os
import sys

FILE_NAME = 'results/statistics_result.tsv'
N=19

def main():

    OUTPUT_FILE = 'results/robustness_checks_output.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    indicator = ['target', 'competitor', 'median_correct_response_latency']
    print("\nLeave-one-participant out (LOPO) Test Result:\n")

    for idct in indicator:

        original_diff_col = f'{idct}_diff'

        mean_diff_row = df[df['sub_id'] == 'Mean Paired Difference']
        original_mean_diff = float (mean_diff_row[original_diff_col].iloc[0])

        original_diff_list = df[original_diff_col].iloc[:19].tolist()
        simu_diff_list = []

        for ignore in range(N):
            sum =0
            for index in range(N):
                if index != ignore:
                    sum += float(original_diff_list[index])

            simu_diff_list.append(sum/(N-1))


   
        plt.figure(figsize=(10, 6))

        participant_ids = list(range(1, N+1))
        bars = plt.bar(participant_ids, simu_diff_list, color='skyblue', edgecolor='black')

        plt.axhline(y=original_mean_diff, color='red', linestyle='--', linewidth=2, label=f'original mean difference = {original_mean_diff:.5f}')

        for bar, val in zip(bars, simu_diff_list):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002, 
                     f'{val:.5f}', ha='center', va='bottom', fontsize=8)

        plt.xlabel('the index of the left subject', fontsize=12)
        plt.ylabel('mean difference (restudy-reprac) from LOPO', fontsize=12)
        plt.title(f'{idct} – result from LOPO', fontsize=14)
        plt.legend()
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.tight_layout()

        script_dir = os.path.dirname(os.path.abspath(FILE_NAME))
        figures_dir = os.path.join(script_dir, 'figures')

        save_path = os.path.join(figures_dir, f'LOPO_{idct}.png')
        plt.savefig(save_path, dpi=300)
        plt.close() 


        # updated : add numerical ouput to txt
        min_val = min(simu_diff_list)
        max_val = max(simu_diff_list)
        std_val = pd.Series(simu_diff_list).std()
        mean_val = pd.Series(simu_diff_list).mean()  


        print(f"\nFor Indicator {idct}: ")
        print(f"Original mean difference (full sample): {original_mean_diff:.5f}")
        print(f"LOPO estimated mean difference (average across 19 leave-outs): {mean_val:.5f}")
        print(f"Range of LOPO estimates: [{min_val:.5f}, {max_val:.5f}]")
        print(f"Standard deviation of LOPO estimates: {std_val:.5f}")
        print(f"Conclusion: All {N} estimates remained {'positive' if min_val > 0 else 'negative' if max_val < 0 else 'mixed in sign'} relative to the original effect.")
        



    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")




    
                          

    

if __name__ == "__main__":
    main()