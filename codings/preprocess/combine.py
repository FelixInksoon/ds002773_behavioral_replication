import csv
import os


def main():
    for sub_id in range(1, 20):
        one_sub(sub_id)


def one_sub(sub_id):

    for run in range(1,4):
        if run == 1:
            new_header, new_rows = one_file(sub_id, run)
        else:
            _, temp_rows = one_file(sub_id, run)
            new_rows.extend(temp_rows)

    output_filename = f'sub-{sub_id:03d}_ses-day3_task-retrieval_combined_events.tsv'
    output_folder = "combined day3_task-retrieval data"
    os.makedirs(output_folder, exist_ok=True)
    
    output_path = os.path.join(output_folder, output_filename)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(new_header)
        writer.writerows(new_rows)



def one_file(sub_id, run):
    with open(f'day3_task-retrieval raw data/sub-{sub_id:03d}_ses-day3_task-retrieval_run-{run}_events.tsv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader) 
        rows = list(reader)

    header.insert(0, 'sub_id')
    for row in rows:
        row.insert(0, sub_id)
    new_header = header
    new_rows = rows
    return new_header, new_rows



if __name__ == "__main__":
    main()


