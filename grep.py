import os
import csv
import pandas as pd

def grep_op_name_to_csv(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if "llama-cli" in line:
                outfile.write(line)
        print(f"Output written to {output_filename}")

def grep_flash_attn_ext(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    with open(output_filename, 'w') as outfile:
        for line in lines:
            if "FLASH_ATTN_EXT" in line:
                outfile.write(line)
        print(f"Output written to {output_filename}")

def grep_firstlast30(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    first_30_lines = lines[:30] 
    last_30_lines = lines[-30:]
    relevant_lines = first_30_lines + last_30_lines

    with open(output_filename, 'w') as outfile:
        for line in first_30_lines:
            outfile.write(line)
        outfile.write("-------------------\n")
        for line in last_30_lines:
            outfile.write(line)
        print(f"Output written to {output_filename}")

def diff_files(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, header=None, on_bad_lines="skip")
        
        df[7] = df[7].diff()

        df.to_csv(output_filename, index=False, header=False,float_format='%.6f')
        print(f"diff file saved as {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_last_column_sum(csv_file):
    total_sum = 0
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                value = float(row[-1])  # Assuming the last column is numeric
                total_sum += value
            except ValueError:
                pass
    
    print(f"Total sum: {total_sum}")


def grepnofa(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, header=None, on_bad_lines="skip")
        grep_results = []
        
        for i in range(len(df)):
            if df.iloc[i, 2] == ' CONT ':
                # Capture the current line and the three lines above it
                start_index = max(0, i - 3)
                sum_column_8 = df.iloc[start_index:i+1, 7].sum()
                
                lines_to_append = df.iloc[start_index:i+1].values.tolist()
                new_line = lines_to_append[-1][:7] + [sum_column_8] + lines_to_append[-1][8:]
                new_line[0] = "sum"
                grep_results.extend(lines_to_append)
                grep_results.append(new_line)    

        grep_df = pd.DataFrame(grep_results)
        grep_df.to_csv(output_filename, index=False, header=False, float_format='%.6f')
        print(f"grepnofa written to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    logs_dir = './logs/'

    # grep_op_name_to_csv(os.path.join(logs_dir, 'fa.log'), os.path.join(logs_dir, 'fa.csv'))
    # grep_firstlast30(os.path.join(logs_dir, 'fa.csv'), os.path.join(logs_dir, 'fa_30.csv'))
    # diff_files(os.path.join(logs_dir, 'fa_30.csv'), os.path.join(logs_dir, 'faop.csv'))
    # grep_flash_attn_ext(os.path.join(logs_dir, 'faop.csv'), os.path.join(logs_dir, 'faoptime.csv'))

    # grep_op_name_to_csv(os.path.join(logs_dir, 'nofa.log'), os.path.join(logs_dir, 'nofa.csv'))
    # grep_firstlast30(os.path.join(logs_dir, 'nofa.csv'), os.path.join(logs_dir, 'nofa_30.csv'))
    # diff_files(os.path.join(logs_dir, 'nofa_30.csv'), os.path.join(logs_dir, 'nofaop.csv'))
    grepnofa(os.path.join(logs_dir, 'nofaop.csv'), os.path.join(logs_dir, 'nofaoptime.csv'))