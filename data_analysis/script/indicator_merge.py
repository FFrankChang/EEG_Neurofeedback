import pandas as pd
import numpy as np
import os

def split_steer_column(data):
    """Split Steer column into three new columns: Steering_Angle, Throttle, Brake."""
    data['Steer'] = data['Steer'].apply(eval)
    data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0])
    data['Throttle'] = data['Steer'].apply(lambda x: x[1])
    data['Brake'] = data['Steer'].apply(lambda x: x[2])
    data.drop('Steer', axis=1, inplace=True)
    return data

def calculate_ttc(data):
    """Calculate TTC (Time to Collision) and update dataset."""
    data['Distance'] = np.sqrt((data['Location_x'] - data['Lead_Vehicle_X'])**2 +
                               (data['Location_y'] - data['Lead_Vehicle_Y'])**2 +
                               (data['Location_z'] - data['Lead_Vehicle_Z'])**2)
    data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed'])
    data['TTC'] = data['Distance'] / data['Relative_Speed'].replace(0, np.inf)
    return data

def merge_datasets(file1_path, file2_path, output_path):
    data1 = pd.read_csv(file1_path)
    data1 = split_steer_column(data1)
    data1 = calculate_ttc(data1)
    
    data2 = pd.read_csv(file2_path)
    merged_data = pd.merge_asof(data1, data2, on='timestamp', direction='nearest')
    merged_data.to_csv(output_path, index=False)

def filter_folder_paths(csv_file_path, date=None, subject=None, experiment_no=None, scenario=None, condition=None):
    data = pd.read_csv(csv_file_path)
    if date:
        data = data[data['Date'] == date]
    if subject:
        data = data[data['Subject'] == subject]
    if experiment_no:
        data = data[data['ExperimentNo'] == experiment_no]
    if scenario:
        data = data[data['Scenario'] == scenario]
    if condition:
        data = data[data['Condition'] == condition]
    return data['FolderPath'].tolist()

def process_folders(folder_paths):
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            carla_files = [f for f in files if 'carla' in f]
            psd_files = [f for f in files if 'psd' in f]
            for carla_file, psd_file in zip(carla_files, psd_files):
                carla_path = os.path.join(root, carla_file)
                psd_path = os.path.join(root, psd_file)
                output_path = os.path.join(root, 'carla_merged.csv')
                merge_datasets(carla_path, psd_path, output_path)
                print(output_path,'success')

# Set directory and process files based on conditions specified in the index CSV
index_csv_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv'

# scenario = 'hard'
folder_paths=filter_folder_paths(index_csv_path)
process_folders(folder_paths)
