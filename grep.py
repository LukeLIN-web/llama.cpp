import os
import csv
import pandas as pd
from io import StringIO

def grep_op_name_to_csv(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if "llama-cli" in line:
                outfile.write(line)
        print(f"grep_op_name_to_csv Output written to {output_filename}")

def grep_flash_attn_ext(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    with open(output_filename, 'w') as outfile:
        for line in lines:
            if "FLASH_ATTN_EXT" in line:
                outfile.write(line)
        print(f"grep_flash_attn_ext Output written to {output_filename}")

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
        print(f"grep_firstlast30 Output written to {output_filename}")

def diff_files(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, header=None, on_bad_lines="skip")
        
        df[7] = df[7].diff()

        df.to_csv(output_filename, index=False, header=False,float_format='%.6f')
        print(f"diff file saved as {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def grepnofa(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, header=None, on_bad_lines="skip")
        grep_results = []
        
        for i in range(len(df)):
            if df.iloc[i, 2] == ' CONT ':
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

def grepbench(input_filename, output_filename):


    with open(input_filename, 'r') as file:
        data_str = file.read()

    data_io = StringIO(data_str)

    # Read the data with delimiter '|'
    reader = csv.reader(data_io, delimiter='|')

    # Skip the first two rows (header and separator)
    next(reader)  # header row
    next(reader)  # separator row

    with open(output_filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["model", "size", "params", "backend", "ngl", "fa", "test", "t/s"])
        for row in reader:
            if len(row) > 1:
                # Extract and clean each field
                fields = [field.strip() for field in row if field.strip()]

                # Split the last field into two columns based on '±' delimiter
                if len(fields) >= 8:
                    last_field = fields[-1]
                    split_fields = last_field.split('±', 1)
                    fields = fields[:-1] + split_fields

                writer.writerow(fields)

    print(f"grep bench data written to {output_filename}")


if __name__ == "__main__":
    logs_dir = './logs/'

    # grep_op_name_to_csv(os.path.join(logs_dir, 'fa.log'), os.path.join(logs_dir, 'fa.csv'))
    # grep_firstlast30(os.path.join(logs_dir, 'fa.csv'), os.path.join(logs_dir, 'fa_30.csv'))
    # diff_files(os.path.join(logs_dir, 'fa_30.csv'), os.path.join(logs_dir, 'faop.csv'))
    # grep_flash_attn_ext(os.path.join(logs_dir, 'faop.csv'), os.path.join(logs_dir, 'faoptime.csv'))

    # grep_op_name_to_csv(os.path.join(logs_dir, 'nofa.log'), os.path.join(logs_dir, 'nofa.csv'))
    # grep_firstlast30(os.path.join(logs_dir, 'nofa.csv'), os.path.join(logs_dir, 'nofa_30.csv'))
    # diff_files(os.path.join(logs_dir, 'nofa_30.csv'), os.path.join(logs_dir, 'nofaop.csv'))
    # grepnofa(os.path.join(logs_dir, 'nofaop.csv'), os.path.join(logs_dir, 'nofaoptime.csv'))
    grepbench(os.path.join(logs_dir, 'bench.log'), os.path.join(logs_dir, 'bench.csv'))