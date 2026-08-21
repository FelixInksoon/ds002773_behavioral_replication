import csv
import os
import statistics

# this program is used for the calculation of the percentage of response type in retprac and restudy task.
# also for median response time for correct responses in retprac and restudy conditions.

# 26.08.09 update: # this file is used to calculate the correct-response latency for each subject and each condition (retrieval practice and restudy) and then calculate the median correct-response latency for each subject and each condition. The output is a tsv file with the median correct-response latency for each subject and each condition.
# the output will be conbined into the summary_percentages.tsv file for further analysis and plotting.

DECIMAL_PLACES = 5

def main():

    

    output_file = 'results/statistics_result.tsv'

    row_names = [
            'sub_id',
            'restudy_target', 'restudy_competitor', 'restudy_other', 'restudy_no_response', 'restudy_don_t_know',
            'retprac_target', 'retprac_competitor', 'retprac_other', 'retprac_no_response', 'retprac_don_t_know',
            'restudy_median_response_time', 'retprac_median_response_time',
            'restudy_median_correct_response_latency', 'retprac_median_correct_response_latency'
        ]

    new_rows = []
    # total_restudy_result_count = [0, 0, 0, 0, 0]
    # total_retprac_result_count = [0, 0, 0, 0, 0]
    # restudy_total = 0
    # retprac_total = 0

    for sub_id in range(1, 20):
        (
            restudy_percentages,
            retprac_percentages,
            # restudy_result_count,
            # retprac_result_count,
            # restudy_temp,
            # retprac_temp,
            restudy_median_response_times_in_target,
            retprac_median_response_times_in_target,
            restudy_median_correct_response_latency,
            retprac_median_correct_response_latency
        ) = one_sub(sub_id)


        new_rows.append([sub_id] + restudy_percentages + retprac_percentages + [restudy_median_response_times_in_target] + [retprac_median_response_times_in_target] + [restudy_median_correct_response_latency] + [retprac_median_correct_response_latency])
        # restudy_total += restudy_temp
        # retprac_total += retprac_temp
        for i in range(5):
            # total_restudy_result_count[i] += restudy_result_count[i]
            # total_retprac_result_count[i] += retprac_result_count[i]
            pass


    # new_rows.append(['total in count'] + total_restudy_result_count + total_retprac_result_count)

    # for i in range(5):
        # total_restudy_result_count[i] = round(total_restudy_result_count[i] / restudy_total, DECIMAL_PLACES)
        # total_retprac_result_count[i] = round(total_retprac_result_count[i] / retprac_total, DECIMAL_PLACES)

    ### print(restudy_total, retprac_total) ### for debugging

    # new_rows.append(['total in percentage'] + total_restudy_result_count + total_retprac_result_count)


    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(row_names)          
        writer.writerows(new_rows) 



def one_sub(sub_id):

    filename = f'raw data/preprocessed_day3_task-retrieval data/sub-{sub_id:03d}_ses-day3_task-retrieval_combined_events.tsv'
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)            
        rows = list(reader)

    tasktype_index = header.index('update_cond')
    response_index = header.index('response_type')
    response_time_index = header.index('response_time')

    restudy_result_count = [0, 0, 0, 0, 0] #target, competitor, other, no response, don't know
    retprac_result_count = [0, 0, 0, 0, 0] #target, competitor, other, no response, don't know

    restudy_result_percentage = [0, 0, 0, 0, 0] 
    retprac_result_percentage = [0, 0, 0, 0, 0] 

    restudy_response_times_in_target = []
    retprac_response_times_in_target = []

    restudy_correct_response_latency = []
    retprac_correct_response_latency = []

    restudy_total = 0
    retprac_total = 0

    for row in rows:
        if row[tasktype_index] == 'restudy':
            restudy_total += 1
            if row[response_index] == 'target':
                restudy_result_count[0] += 1
                restudy_response_times_in_target.append(float(row[response_time_index]))
                restudy_correct_response_latency.append(float(row[response_time_index]))
            elif row[response_index] == 'competitor':
                restudy_result_count[1] += 1
            elif row[response_index] == 'other':
                restudy_result_count[2] += 1
            elif row[response_index] == 'no response':
                restudy_result_count[3] += 1
            elif row[response_index] == "don't know":
                restudy_result_count[4] += 1

        elif row[tasktype_index] == 'retprac':
            retprac_total += 1
            if row[response_index] == 'target':
                retprac_result_count[0] += 1
                retprac_response_times_in_target.append(float(row[response_time_index]))
                retprac_correct_response_latency.append(float(row[response_time_index]))
            elif row[response_index] == 'competitor':
                retprac_result_count[1] += 1
            elif row[response_index] == 'other':
                retprac_result_count[2] += 1
            elif row[response_index] == 'no response':
                retprac_result_count[3] += 1
            elif row[response_index] == "don't know":
                retprac_result_count[4] += 1

    for i in range(5):
        restudy_result_percentage[i] = round(restudy_result_count[i] / restudy_total, DECIMAL_PLACES)
        retprac_result_percentage[i] = round(retprac_result_count[i] / retprac_total, DECIMAL_PLACES)

    restudy_median_response_times_in_target = statistics.median(restudy_response_times_in_target)
    retprac_median_response_times_in_target = statistics.median(retprac_response_times_in_target)

    restudy_median_correct_response_latency = statistics.median(restudy_correct_response_latency)
    retprac_median_correct_response_latency = statistics.median(retprac_correct_response_latency)




    return (
        restudy_result_percentage,
        retprac_result_percentage,
        # restudy_result_count,
        # retprac_result_count,
        # restudy_total,
        # retprac_total,
        restudy_median_response_times_in_target,
        retprac_median_response_times_in_target,
        restudy_median_correct_response_latency,
        retprac_median_correct_response_latency
    )

if __name__ == "__main__":
    main()


