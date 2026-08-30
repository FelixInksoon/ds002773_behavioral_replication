# this file is used to add three new reduction:
# other, don't know, no response

# add_reduction_columns.py
# 读取 statistics_result.tsv，为前 19 行添加三个 reduction 列，保存为新文件或覆盖原文件

import pandas as pd

FILE_NAME = 'results/statistics_result.tsv'
OUTPUT_FILE = 'results/statistics_result.tsv'  

def main():
    
    df = pd.read_csv(FILE_NAME, sep='\t')

    df['other reduction'] = pd.NA
    df["don't know reduction"] = pd.NA
    df['no response reduction'] = pd.NA

    
    participant_rows = df.iloc[:19]  
    
    other_reduction_values = participant_rows['restudy_other'] - participant_rows['retprac_other']
    dont_know_reduction_values = participant_rows['restudy_don_t_know'] - participant_rows['retprac_don_t_know']
    no_response_reduction_values = participant_rows['restudy_no_response'] - participant_rows['retprac_no_response']

    df.loc[:18, 'other reduction'] = other_reduction_values
    df.loc[:18, "don't know reduction"] = dont_know_reduction_values
    df.loc[:18, 'no response reduction'] = no_response_reduction_values

    df.to_csv(OUTPUT_FILE, sep='\t', index=False)

if __name__ == "__main__":
    main()