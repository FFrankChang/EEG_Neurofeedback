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
    if steer_change_timestamp != "No change detected":
        steer_change_timestamp = datetime.fromtimestamp(steer_change_timestamp, beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')

    # Step 2: Find all timestamps where Mode_Switched is "Yes"
    mode_switched_timestamps = data[data['Mode_Switched'] == "Yes"]['timestamp'].tolist()
    mode_switched_timestamps = [datetime.fromtimestamp(ts, beijing_timezone).strftime('%Y-%m-%d %H:%M:%S') for ts in mode_switched_timestamps]

    return steer_change_timestamp, mode_switched_timestamps

def process_folder(directory_path):
    # Find all csv files that start with 'carla_'
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.startswith('carla_') and f.endswith('.csv')]
    
    results = {}
    for file in files:
        steer_change, mode_switched = detect_changes(file)
        results[file] = {
            "Steer change timestamp": steer_change,
            "Mode_Switched timestamps": mode_switched
        }
    return results

# Example usage
directory_path = 'path_to_your_directory'
results = process_folder(directory_path)
for file, result in results.items():
    print(f"File: {file}")
    print(f"Timestamp when Steer data starts changing: {result['Steer change timestamp']}")
    print(f"Timestamps when Mode_Switched is 'Yes': {result['Mode_Switched timestamps']}")
    print(result['Mode_Switched timestamps']-result['Steer change timestamp'])
