import pandas as pd
import os
from datetime import datetime, timedelta, timezone

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

def detect_changes(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Adjusting for Beijing Time (UTC+8)
    beijing_timezone = timezone(timedelta(hours=8))

    # Step 1: Detect when Steer changes
    fixed_steer = "(0.0, 0.5, 0.5)"
    steer_change_index = data[data['Steer'] != fixed_steer].index[0] if not data[data['Steer'] != fixed_steer].empty else None
    steer_change_timestamp = data.loc[steer_change_index, 'timestamp'] if steer_change_index is not None else "No change detected"
 
    mode_switched_timestamp = data.loc[data['Mode_Switched'] == "Yes", 'timestamp'].iloc[0]
    return steer_change_timestamp, mode_switched_timestamp

def process_folder(directory_path):
    for filename in os.listdir(directory_path):
        if filename.startswith('carla_2024') and filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            break
    steer_change, mode_switched = detect_changes(file_path)
    return steer_change,mode_switched

# Example usage     
directory_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv'
folder= filter_folder_paths(directory_path)
results = []
for item in folder:
    steer_change,mode_switched= process_folder(item)
    # print(item,mode_switched-steer_change)
    results.append([item,mode_switched-steer_change])
df = pd.DataFrame(results, columns=['Item', 'Result'])
df.to_csv('gap_detection.csv',index=False)