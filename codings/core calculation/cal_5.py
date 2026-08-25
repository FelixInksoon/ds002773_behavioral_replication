# this file is used to make ANOVA and LMM of Condition * Runs
import pandas as pd
from statsmodels.formula.api import mixedlm
from statsmodels.stats.anova import AnovaRM
import os
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

FILE_NAME = 'results/statistics_result_in_runs.tsv'

def main():

    OUTPUT_FILE = 'results/run-level_results.txt'
    log_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
    sys.stdout = log_file

    df = pd.read_csv(FILE_NAME, sep='\t')
    
    target_cols = ['restudy_target', 'retrieval_target']
    df_target = df.melt(
        id_vars=['sub_id', 'run_id'],
        value_vars=target_cols,
        var_name='condition',
        value_name='target_accuracy'
    )
    df_target['condition'] = df_target['condition'].map({
        'restudy_target': 'restudy',
        'retrieval_target': 'retrieval'
    })

    ### print(df_target)
    
    competitor_cols = ['restudy_competitor', 'retrieval_competitor']
    df_competitor = df.melt(
        id_vars=['sub_id', 'run_id'],
        value_vars=competitor_cols,
        var_name='condition',
        value_name='competitor_accuracy'
    )
    df_competitor['condition'] = df_competitor['condition'].map({
        'restudy_competitor': 'restudy',
        'retrieval_competitor': 'retrieval'
    })
    

    rt_cols = ['restudy_median_correct_response_latency', 'retrieval_median_correct_response_latency']
    df_rt = df.melt(
        id_vars=['sub_id', 'run_id'],
        value_vars=rt_cols,
        var_name='condition',
        value_name='median_rt'
    )
    df_rt['condition'] = df_rt['condition'].map({
        'restudy_median_correct_response_latency': 'restudy',
        'retrieval_median_correct_response_latency': 'retrieval'
    })
    

    df_long = df_target.merge(df_competitor, on=['sub_id', 'run_id', 'condition']) \
                       .merge(df_rt, on=['sub_id', 'run_id', 'condition'])
    

    df_long['sub_id'] = df_long['sub_id'].astype('category')
    df_long['run_id'] = df_long['run_id'].astype('category')
    df_long['condition'] = df_long['condition'].astype('category')

    # print(df_long)

    for dep, name in [('target_accuracy', 'target recall'),
                      ('competitor_accuracy', 'competitor intrusion'),
                      ('median_rt', 'correct response latency')]:
        analyze_anova(dep, name, df_long=df_long)


    sys.stdout = sys.__stdout__
    log_file.close()

    print("finish")



def analyze_anova(dep_var, dep_name, df_long):

    print(f"ANOVA: {dep_name} ({dep_var})")

    res = AnovaRM(df_long, depvar=dep_var, subject='sub_id', 
                  within=['condition', 'run_id'], aggregate_func='mean').fit()
    
    print(res)
    return res

if __name__ == '__main__':

    main()