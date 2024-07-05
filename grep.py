import os
import csv

def grep_op_name_to_csv(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if "llama-cli" in line:
                outfile.write(line)

def grep_flash_attn_ext(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if "FLASH_ATTN_EXT" in line:
                outfile.write(line)



def remove_columns_from_csv(input_filename, output_filename, columns_to_remove):
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            new_row = [col for idx, col in enumerate(row) if idx not in columns_to_remove]
            writer.writerow(new_row)

if __name__ == "__main__":
    logs_dir = './logs/'
    grep_op_name_to_csv(os.path.join(logs_dir, 'fa.log'), os.path.join(logs_dir, 'fa.csv'))
    grep_flash_attn_ext(os.path.join(logs_dir, 'fa.csv'), os.path.join(logs_dir, 'faop.csv'))
    # remove_columns_from_csv(os.path.join(logs_dir, 'fa.csv'), os.path.join(logs_dir, 'fa_filtered.csv'), [0, 2])