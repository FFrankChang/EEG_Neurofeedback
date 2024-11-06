import pandas as pd
import os

def filter_data(file_path, subfolder_path):
    data = pd.read_csv(file_path)
    
    filtered_data = data.dropna(subset=['reaction_time_10'])
    file_name = os.path.basename(file_path)
    new_file_name = f"{file_name[:-4]}_filter10.csv"
    new_file_path = os.path.join(subfolder_path, new_file_name)
    
    filtered_data.to_csv(new_file_path, index=False)
    return new_file_path

def batch_process(folder_path):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            for file in os.listdir(subfolder_path):
                if 'event' in file and file.endswith('.csv') and 'filter' not in file:
                    file_path = os.path.join(subfolder_path, file)
                    new_file_path = filter_data(file_path, subfolder_path)
                    print(f'Filtered and saved new file: {new_file_path}')

folder_path = r'G:\Exp_V0_data\data'  
batch_process(folder_path)
