import pandas as pd
import os
import glob

def calculate_acceleration_stats(data):
    data['timestamp'] = pd.to_numeric(data['timestamp'], errors='coerce')
    data['Acceleration'] = pd.to_numeric(data['Acceleration'], errors='coerce')

    data['Acceleration_change_rate'] = data['Acceleration'].diff() / data['timestamp'].diff()
    acceleration_x_mean = data['Acceleration'].mean()
    acceleration_x_std = data['Acceleration'].std()
    acceleration_x_change_rate_mean = data['Acceleration_change_rate'].mean()
    return acceleration_x_mean, acceleration_x_std, acceleration_x_change_rate_mean

def extract_filename_data(filename):
    parts = os.path.basename(filename).split('_')
    scenario = parts[1]
    subject = parts[2]
    day = parts[3]
    condition = parts[4] if "silence" in parts[4] else "feedback"
    experiment_time = parts[5].split('.')[0]
    return scenario, subject, day, condition, experiment_time

def process_file(file_path):
    filename = os.path.basename(file_path)
    data = pd.read_csv(file_path)

    acceleration_x_mean, acceleration_x_std, acceleration_x_change_rate_mean = calculate_acceleration_stats(data)
    scenario, subject, day, condition, experiment_time = extract_filename_data(filename)

    return [filename, scenario, subject, day, condition, experiment_time, acceleration_x_mean, acceleration_x_std, acceleration_x_change_rate_mean]

def main():
    root_folder_path = r'E:\NFB_data_backup\20240730'  # Update the root folder path
    subject_folders = glob.glob(os.path.join(root_folder_path, '*'))  # List all subfolders
    
    for folder in subject_folders:
        file_paths = glob.glob(os.path.join(folder, '*carla*C02*.csv'))
        results = []
        for file_path in file_paths:
            result = process_file(file_path)
            results.append(result)

        results_df = pd.DataFrame(results, columns=["Filename", "Scenario", "Subject", "Day", "Condition", "Experiment_Time", "Acceleration_x_Mean", "Acceleration_x_STD", "Acceleration_x_Change_Rate_Mean"])
        results_filename = os.path.basename(folder) + '_C02_results.csv'
        results_df.to_csv(os.path.join(folder, results_filename), index=False)

if __name__ == "__main__":
    main()
