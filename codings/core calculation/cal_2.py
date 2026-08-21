# this file is used to further process the statistics_result.tsv file
# to get these statistics below: Mean, Standard Deviation, Mean Paired Difference, t statistic, p value, Cohen's d, and 95% Confidence Interval 
# for the three indicators: target_recall(percentage), competitor_intrusions(percentage), and median_correct_response_latency
# in two conditions: retrieval practice and restudy. (or diffrence when making pairs)

import csv
import statistics
from scipy import stats
import pandas as pd
import numpy as np

FILE_NAME = 'results/statistics_result.tsv'
N=19

def main():

    df = pd.read_csv(FILE_NAME, sep='\t')
    df = pd.DataFrame(df)

    print(df)


    # Mean&SD
    mean_row = {}
    SD_row = {}

    for idct in ['target', 'competitor', 'median_correct_response_latency']:
        restudy_col = f'restudy_{idct}'
        retprac_col = f'retprac_{idct}'

        mean_row[restudy_col] = f'{df[restudy_col].mean():.5f}'
        SD_row[restudy_col] = f'{df[restudy_col].std():.5f}'

        mean_row[retprac_col] = f'{df[retprac_col].mean():.5f}'
        SD_row[retprac_col] = f'{df[retprac_col].std():.5f}'

    df['target_diff'] =  df['restudy_target'] - df['retprac_target']
    df['competitor_diff'] = df['restudy_competitor'] - df['retprac_competitor']
    df['median_correct_response_latency_diff'] = df['restudy_median_correct_response_latency'] - df['retprac_median_correct_response_latency']
    
    mean_diff_row = {}
    t_statistic_row = {}
    p_value_row = {}
    cohen_d_row = {}
    confidence_interval_row = {}

    for idct in ['target', 'competitor', 'median_correct_response_latency']:
        diff_col = f'{idct}_diff'
        mean_diff = df[diff_col].mean()
        mean_diff_row[diff_col] = mean_diff
        SD_diff = df[diff_col].std()

        t_statistic, p_value = stats.ttest_rel(df[f'restudy_{idct}'], df[f'retprac_{idct}'])
        t_statistic_row[diff_col] = f'{t_statistic:.5f}'
        p_value_row[diff_col] = f'{p_value:.5f}'

        cohen_d = t_statistic / np.sqrt(N) ### or cohen_d = mean_diff / SD_diff
        cohen_d_row[diff_col] = f'{cohen_d:.5f}'

        confidence_interval = stats.t.interval(0.95, N-1, loc=mean_diff, scale=SD_diff/np.sqrt(N))
        confidence_interval_row[diff_col] = f'({confidence_interval[0]:.5f}, {confidence_interval[1]:.5f})'


    
    mean_row['sub_id'] = 'Mean'
    SD_row['sub_id'] = 'SD'

    df.loc['Mean'] = pd.Series(mean_row)
    df.loc['SD'] = pd.Series(SD_row)

    mean_diff_row['sub_id'] = 'Mean Paired Difference'
    t_statistic_row['sub_id'] = 't statistic'
    p_value_row['sub_id'] = 'p value'
    cohen_d_row['sub_id'] = "Cohen's d"
    confidence_interval_row['sub_id'] = '95% Confidence Interval'

    df.loc['Mean Paired Difference'] = pd.Series(mean_diff_row)
    df.loc['t_statistic'] = pd.Series(t_statistic_row)
    df.loc['p_value'] = pd.Series(p_value_row)
    df.loc['cohen_d'] = pd.Series(cohen_d_row)
    df.loc['confidence_interval'] = pd.Series(confidence_interval_row)




    df.to_csv(FILE_NAME, sep='\t', index=False)

if __name__ == '__main__':
    main()