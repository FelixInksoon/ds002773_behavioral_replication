# this file is used to calculate target recall, competitor intrusions, and median correct-response latency separately 
# for each run and for each condition in 19 subjects.
# also this file is used to offer figures showing these variables
import csv
import os
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



DECIMAL_PLACES = 5
FILE_NAME = 'statistics_result_in_runs.tsv'
OUTPUT_DIR = 'figures'

def main():

    

    output_file = 'statistics_result_in_runs.tsv'

    row_names = [
            'sub_id', 'run_id',
            'restudy_target','retrieval_target', 
            'restudy_competitor','retrieval_competitor',
            'restudy_median_correct_response_latency',
            'retrieval_median_correct_response_latency'
        ]

    new_rows = []

    for sub_id in range(1, 20):

        for run_id in range(1,4):

            (
                restudy_target, retrieval_target,                
                restudy_competitor, retrieval_competitor,
                restudy_median_correct_response_latency,
                retrieval_median_correct_response_latency
            ) = one_sub(sub_id, run_id)

            new_rows.append( [sub_id] + [run_id] +
                [restudy_target] + [retrieval_target] +                
                [restudy_competitor] + [retrieval_competitor] + 
                [restudy_median_correct_response_latency] +
                [retrieval_median_correct_response_latency]
            )


    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(row_names)          
        writer.writerows(new_rows) 



    draw()



def one_sub(sub_id, run_id):

    filename = f'day3_task-retrieval raw data/sub-{sub_id:03d}_ses-day3_task-retrieval_run-{run_id}_events.tsv'
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)            
        rows = list(reader)

    condtype_index = header.index('update_cond')
    response_index = header.index('response_type')
    tasktype_index = header.index('task_type')
    response_time_index = header.index('response_time')

    restudy_result_count = [0, 0, 0, 0, 0] #target, competitor
    retrieval_result_count = [0, 0, 0, 0, 0] #target, competitor

    restudy_correct_response_latency = []
    retprac_correct_response_latency = []

    restudy_total = 0
    retrieval_total = 0

    for row in rows:
        if row[condtype_index] == 'restudy' and row[tasktype_index] == 'retrieval':
            restudy_total += 1
            if row[response_index] == 'target':
                restudy_result_count[0] += 1
                restudy_correct_response_latency.append(float(row[response_time_index]))
            elif row[response_index] == 'competitor':
                restudy_result_count[1] += 1

        elif row[condtype_index] == 'retprac' and row[tasktype_index] == 'retrieval':
            retrieval_total += 1
            if row[response_index] == 'target':
                retrieval_result_count[0] += 1

                retprac_correct_response_latency.append(float(row[response_time_index]))
            elif row[response_index] == 'competitor':
                retrieval_result_count[1] += 1

    restudy_target = round(restudy_result_count[0] / restudy_total, ndigits=DECIMAL_PLACES)
    restudy_competitor = round(restudy_result_count[1] / restudy_total, ndigits=DECIMAL_PLACES)

    retrieval_target = round(retrieval_result_count[0] / retrieval_total, ndigits=DECIMAL_PLACES)
    retrieval_competitor = round(retrieval_result_count[1] / retrieval_total, ndigits=DECIMAL_PLACES)

    restudy_median_correct_response_latency = statistics.median(restudy_correct_response_latency)
    retrieval_median_correct_response_latency = statistics.median(retprac_correct_response_latency)




    return (
        restudy_target, retrieval_target,                
        restudy_competitor, retrieval_competitor,
        restudy_median_correct_response_latency,
        retrieval_median_correct_response_latency
    )


def draw():
    df = pd.read_csv(FILE_NAME, sep='\t')
    
    metrics = [
        ('target', 'target recall'),
        ('competitor', 'competitor_intrusion'),
        ('median_correct_response_latency', 'median correct response latency')
    ]
    
    
    nrows, ncols = 4, 5
    total_subplots = nrows * ncols
    subjects = sorted(df['sub_id'].unique())
    
    for col_prefix, label in metrics:

        restudy_col = f'restudy_{col_prefix}'
        retrieval_col = f'retrieval_{col_prefix}'
        all_vals = pd.concat([df[restudy_col], df[retrieval_col]]).dropna()
        
        if len(all_vals) == 0:
            y_min, y_max = 0, 1
        else:
            y_min = all_vals.min()
            y_max = all_vals.max()

            margin = (y_max - y_min) * 0.1 
            y_min = max(0, y_min - margin)  
            y_max = y_max + margin
        
        fig, axes = plt.subplots(nrows, ncols, figsize=(15, 10))
        axes_flat = axes.flatten()
        
        for idx, sub_id in enumerate(subjects):
            ax = axes_flat[idx]
            sub_df = df[df['sub_id'] == sub_id].sort_values('run_id')
            
     
            ax.plot(sub_df['run_id'], sub_df[restudy_col],
                    color='blue', linestyle='-', linewidth=1.5, marker='o', markersize=4,
                    label='Restudy' if idx == 0 else "")

            ax.plot(sub_df['run_id'], sub_df[retrieval_col],
                    color='red', linestyle='--', linewidth=1.5, marker='s', markersize=4,
                    label='Retrieval' if idx == 0 else "")
            

            ax.set_ylim(y_min, y_max)
            
            ax.set_title(f'Sub-{int(sub_id)}', fontsize=9)
            ax.set_xticks([1, 2, 3])
            ax.tick_params(axis='both', labelsize=7)

            if idx % ncols == 0:
                ax.set_ylabel(label, fontsize=8)
            if idx >= (nrows - 1) * ncols:
                ax.set_xlabel('Run', fontsize=8)
            ax.grid(True, linestyle=':', alpha=0.5)
        

        for idx in range(len(subjects), total_subplots):
            fig.delaxes(axes_flat[idx])
        

        handles, labels = axes_flat[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right', fontsize=10)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        plt.tight_layout(rect=[0, 0, 0.95, 0.95])
        save_path = os.path.join(OUTPUT_DIR, f'{col_prefix}_small_multiples.png')
        plt.savefig(save_path, dpi=300)
        plt.close(fig)





if __name__ == "__main__":
    main()


