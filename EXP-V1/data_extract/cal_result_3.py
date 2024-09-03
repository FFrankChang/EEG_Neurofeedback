import pandas as pd
import numpy as np
import os
import glob

def split_steer_column(data):
    data['Steer'] = data['Steer'].apply(lambda x: eval(x))
    data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0]*540)
    data['Throttle'] = data['Steer'].apply(lambda x: x[1])
    data['Brake'] = data['Steer'].apply(lambda x: x[2])
    data.drop('Steer', axis=1, inplace=True)
    return data

def calculate_ttc(data):
    data['Distance'] = np.sqrt((data['Location_x'] - data['Lead_Vehicle_X'])**2 +
                               (data['Location_y'] - data['Lead_Vehicle_Y'])**2 +
                               (data['Location_z'] - data['Lead_Vehicle_Z'])**2)
    data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed'])
    data['TTC'] = data['Distance'] / data['Relative_Speed'].replace(0, np.inf)
    return data

def calculate_road_exits(data):
    data['On_Road'] = (data['Location_y'] >= 2992.5) & (data['Location_y'] <= 3000)
    transitions = data['On_Road'].astype(int).diff().ne(0)
    road_exits = ((transitions) & (data['On_Road'].shift(-1) == False)).sum()
    return road_exits

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
    data = split_steer_column(data)
    data = calculate_ttc(data)
    road_exits = calculate_road_exits(data)

    first_yes_index = data[data['TOR'] == 'Yes'].index[0]
    data_post_tor_yes = data.loc[first_yes_index:]
    min_ttc = data_post_tor_yes['TTC'].min()
    steering_angle_std = data_post_tor_yes['Steering_Angle'].abs().std()
    acceleration_x_mean = data_post_tor_yes['Acceleration_x'].mean()
    acceleration_x_std = data_post_tor_yes['Acceleration_x'].std()
    data_post_tor_yes['Acceleration_x_change_rate'] = data_post_tor_yes['Acceleration_x'].diff() / data_post_tor_yes['timestamp'].diff()
    acceleration_x_change_rate_mean = data_post_tor_yes['Acceleration_x_change_rate'].mean()

    scenario, subject, day, condition, experiment_time = extract_filename_data(filename)

    return [filename, scenario, subject, day, condition, experiment_time, min_ttc, steering_angle_std, acceleration_x_mean, acceleration_x_std, acceleration_x_change_rate_mean, road_exits]

def main():
    root_folder_path = r'E:\NFB_data_backup\filtered'  # Update the root folder path
    subject_folders = glob.glob(os.path.join(root_folder_path, '*'))  # List all subfolders
    
    for folder in subject_folders:
        file_paths = glob.glob(os.path.join(folder, '*carla*c01*.csv'))
        results = []
        for file_path in file_paths:
            result = process_file(file_path)
            results.append(result)

        results_df = pd.DataFrame(results, columns=["Filename", "Scenario", "Subject", "Day", "Condition", "Experiment_Time", "Min_TTC", "Steering_Angle_STD", "Acceleration_x_Mean", "Acceleration_x_STD", "Acceleration_x_Change_Rate_Mean", "Road_Exits"])
        results_filename = os.path.basename(folder) + '_results.csv'
        results_df.to_csv(os.path.join(folder, results_filename), index=False)

if __name__ == "__main__":
    main()
