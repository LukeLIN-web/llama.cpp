import os
import csv
import pandas as pd
import re
import sys
from io import StringIO

def grep_op_name_to_csv(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if "llama-cli" in line and line.count(',') == 7:
                outfile.write(line)
        print(f"grep_op_name_to_csv Output written to {output_filename}")
    try:
        df = pd.read_csv(output_filename, header=None, on_bad_lines="skip")
        df[7] = df[7].diff()
        df.to_csv(output_filename, index=False, header=False,float_format='%.6f')
        print(f"diff file saved as {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

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
                sum_column_7 = df.iloc[start_index:i+1, 7].sum()
                
                lines_to_append = df.iloc[start_index:i+1].values.tolist()
                new_line = lines_to_append[-1][:7] + [sum_column_7] + lines_to_append[-1][8:]
                new_line[0] = "sum"
                grep_results.extend(lines_to_append)
                grep_results.append(new_line)    

        firstlayer = df.iloc[0:24, 7].sum()
        lastlayer = df.iloc[-27:-2, 7].sum()        

        print(f"first layer time : {firstlayer}")
        print(f"Last layer time: {lastlayer}")
        
        grep_df = pd.DataFrame(grep_results)
        grep_df.to_csv(output_filename, index=False, header=False, float_format='%.6f')
        print(f"grepnofa written to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def grepbench(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        data_str = file.read()

    data_io = StringIO(data_str)
    reader = csv.reader(data_io, delimiter='|')

    next(reader)  # header row
    next(reader)  # separator row

    with open(output_filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["model", "size", "params", "backend", "ngl", "fa", "test", "t/s"])
        for row in reader:
            if len(row) > 1:
                fields = [field.strip() for field in row if field.strip()]

                if len(fields) >= 8:
                    last_field = fields[-1]
                    split_fields = last_field.split('±', 1)
                    fields = fields[:-1] + split_fields

                writer.writerow(fields)

    print(f"grep bench data written to {output_filename}")

def extract_last(input_filename,output_filename):
    extracted_numbers = []
    tgnum = []
    line_step = 5

    with open(input_filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), line_step):
            if i < len(lines):
                floats = re.findall(r'\d+\.\d+', lines[i])
                if floats:
                    last_float = float(floats[-1])  # Find all floats and get the last one
                    extracted_numbers.append(last_float)
        for i in range(1, len(lines), line_step):
            if i < len(lines):
                floats = re.findall(r'\d+\.\d+', lines[i])
                if floats:
                    last_float = float(floats[-1])  # Find all floats and get the last one
                    tgnum.append(last_float)

    ppavg = sum(extracted_numbers) / len(extracted_numbers)
    tgavg = sum(tgnum) / len(tgnum)

    with open(output_filename, 'a') as file:
        file.write(f"input_filename, {input_filename}\n")
        file.write(f"pp Average, {ppavg:.2f}\n")
        file.write(f"tg Average, {tgavg:.2f}\n")


def grep4opslayers(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, header=None, on_bad_lines="skip")
        
        sums = []
        num_rows = len(df) # 725
        for i in range(num_rows - 725 - 2 - 13 , num_rows - 2 - 13, 23): #  last block
            layersum = df.iloc[i:i+23, 7].sum()
            fouropsum = df.iloc[i+8:i+12, 7].sum()
            # print(df.iloc[i+8:i+12, 2])
            print(df.iloc[i:i+23, 7])
            # print(fouropsum)
            print(layersum)
            sums.append(fouropsum/layersum)

        with open(output_filename, 'w') as f:
            for sum_value in sums:
                f.write(f"{sum_value}\n")
        print(f"greplayers written to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def grepfaoplayers(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, header=None, on_bad_lines="skip")
        
        sums = []
        num_rows = len(df) # 725
        for i in range(num_rows - 725 - 2 - 20 , num_rows - 2-11, 20): #  last block
            layersum = df.iloc[i:i+20, 7].sum()
            print(df.iloc[i+11, 2])
            sums.append(df.iloc[i+11, 7]/layersum)

        with open(output_filename, 'w') as f:
            for sum_value in sums:
                f.write(f"{sum_value}\n")
        print(f"greplayers written to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    logs_dir = './logs/'
    input_filename = sys.argv[1]

    input_filename_part = input_filename[13:16]

    grep_op_name_to_csv(input_filename, os.path.join(logs_dir, f'{input_filename_part}.csv'))
    grep_firstlast30(os.path.join(logs_dir, f'{input_filename_part}.csv'), os.path.join(logs_dir, f'{input_filename_part}_30.csv'))
    if input_filename_part[0] =="1":
        grep_flash_attn_ext(os.path.join(logs_dir, f'{input_filename_part}op.csv'), os.path.join(logs_dir, f'{input_filename_part}optime.csv'))
        grepfaoplayers(os.path.join(logs_dir, f'{input_filename_part}.csv'), os.path.join(logs_dir, f'{input_filename_part}layers.csv'))
    else:
        grepnofa(os.path.join(logs_dir, f'{input_filename_part}op.csv'), os.path.join(logs_dir, f'{input_filename_part}optime.csv'))
        grep4opslayers(os.path.join(logs_dir, f'{input_filename_part}.csv'), os.path.join(logs_dir, f'{input_filename_part}layers.csv'))
    
    
    # grepbench(os.path.join(logs_dir, 'bench.log'), os.path.join(logs_dir, 'bench.csv'))
    # extract_last(input_filename,os.path.join(logs_dir, 'avgtime.csv'))