import pandas as pd
import os

def count_rows(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Calculate total number of rows
    total_rows = len(data)
    
    # Calculate 'Traffic Rows' and 'Simple Rows'
    if 'scenario' in data.columns:
        traffic_rows = (data['scenario'] == 'traffic').sum()
        simple_rows = (data['scenario'] == 'simple').sum()
    else:
        traffic_rows = 'N/A'
        simple_rows = 'N/A'
    
    return total_rows, traffic_rows, simple_rows

def batch_process(folder_path):
    total = 0
    traffic = 0
    simple = 0

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            # Process each CSV file in the subfolder
            for file in os.listdir(subfolder_path):
                if 'event' in file and file.endswith('.csv') and 'filter4' in file:
                    file_path = os.path.join(subfolder_path, file)
                    total_rows, traffic_rows, simple_rows = count_rows(file_path)
                    total+=total_rows
                    traffic+=traffic_rows
                    simple+=simple_rows
                    print(f'{file}: Total = {total_rows}, Traffic = {traffic_rows}, Simple = {simple_rows}')

    print(f'SUM-----Total = {total}, Traffic = {traffic}, Simple = {simple}')

# Example usage
folder_path = r'G:\Exp_V0_data\data'
batch_process(folder_path)
