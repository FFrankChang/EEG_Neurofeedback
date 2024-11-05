import pandas as pd
import os
import glob

def process_events_complete(df):
    df['timestamp_mo'] = pd.to_datetime(df['timestamp'], unit='s')
    df.sort_values('timestamp_mo', inplace=True)
    df['diff_seconds'] = df['timestamp_mo'].diff().dt.total_seconds()
    last_true_index = None
    modified_count = 0
    modified_timestamps = []
    modified_index = []

    for i in df.index:
        if df.at[i, 'event_triggered']:
            if last_true_index is None or (df.at[i, 'timestamp_mo'] - df.at[last_true_index, 'timestamp_mo']).total_seconds() >= 3:
                last_true_index = i
            else:
                df.at[i, 'event_triggered'] = False
                modified_count += 1
                modified_timestamps.append(df.at[i, 'timestamp_mo'])
                modified_index.append(i)
    df.drop(columns=['diff_seconds'], inplace=True)
    df.drop(columns=['timestamp_mo'], inplace=True)
    
    return modified_count, modified_timestamps, modified_index

def process_folder(folder_path):
    # Find all CSV files containing 'C04' in their filenames within the given folder and subfolders
    csv_files = glob.glob(folder_path + '/**/*C04*.csv', recursive=True)

    for file_path in csv_files:
        data = pd.read_csv(file_path)
        modified_count, modified_timestamps, modified_index = process_events_complete(data)

        # Save the cleaned data back to the same file
        data.to_csv(file_path, index=False)

        # Optionally, print information about each file processed
        print(f"Processed {file_path}:")
        print(f"Number of modifications: {modified_count}")
        print("Modified index:", modified_index)

# Specify the directory path
folder_path = r"G:\Exp_V0_data"
process_folder(folder_path)
