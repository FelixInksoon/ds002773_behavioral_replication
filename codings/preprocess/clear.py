import csv
from email import header
import os


def main():

    for sub_id in range(1, 20):
        one_sub(sub_id)


def one_sub(sub_id):

    filename = f'combined day3_task-retrieval data/sub-{sub_id:03d}_ses-day3_task-retrieval_combined_events.tsv'
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)            
        rows = list(reader)              
    clear_index = header.index('task_type')
    new_rows = []
    for row in rows:
        if row[clear_index] == 'retrieval':
            new_rows.append(row)

    output_path = f'preprocessed_day3_task-retrieval data/sub-{sub_id:03d}_ses-day3_task-retrieval_combined_events.tsv'
    os.makedirs('preprocessed_day3_task-retrieval data', exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(header)          
        writer.writerows(new_rows)  



if __name__ == "__main__":
    main()


