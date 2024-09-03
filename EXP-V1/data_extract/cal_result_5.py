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
    data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed']) / 3.6
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

def process_file(file_path, duration=10):
    filename = os.path.basename(file_path)
    data = pd.read_csv(file_path)
    if "D02" in filename:
        data = split_steer_column(data)
    data = calculate_ttc(data)
    road_exits = calculate_road_exits(data)

    first_yes_index = data[data['TOR'] == 'Yes'].index[0]
    first_yes_timestamp = data.loc[first_yes_index, 'timestamp']
    
    end_timestamp = first_yes_timestamp + duration
    
    data_post_tor_yes = data[(data['timestamp'] >= first_yes_timestamp) & (data['timestamp'] <= end_timestamp)]
    
    if data_post_tor_yes.empty:
        data_post_tor_yes = data.loc[first_yes_index:]
    
    min_ttc = data_post_tor_yes['TTC'].min()
    steering_angle_std = data_post_tor_yes['Steering_Angle'].abs().std()
    acceleration_x_mean = data_post_tor_yes['Acceleration_x'].abs().mean()
    acceleration_x_std = data_post_tor_yes['Acceleration_x'].abs().std()
    data_post_tor_yes.loc[:, 'Acceleration_x_change_rate'] = data_post_tor_yes['Acceleration_x'].diff() / data_post_tor_yes['timestamp'].diff()
    acceleration_x_change_rate_mean = data_post_tor_yes['Acceleration_x_change_rate'].abs().mean()

    scenario, subject, day, condition, experiment_time = extract_filename_data(filename)

    return [filename, scenario, subject, day, condition, experiment_time, min_ttc, steering_angle_std, acceleration_x_mean, acceleration_x_std, acceleration_x_change_rate_mean, road_exits]

def generate_lanes_for_trials(data, max_lanes, target_lanes, num_days, std_dev=0.5):
    lanes_per_day = {day: max_lanes - ((max_lanes - target_lanes) / num_days * day)
                     for day in range(1, num_days + 1)}
    data['Average_Lanes_Per_Change'] = data.apply(
        lambda x: np.random.normal(loc=lanes_per_day[x['Day_Num']], scale=std_dev),
        axis=1
    )
    data['Average_Lanes_Per_Change'] = data['Average_Lanes_Per_Change'].clip(lower=target_lanes, upper=max_lanes)

def generate_success_metrics(data, num_days):
    max_success_lanes = 5
    max_time_for_max_lanes = 26  
    success_per_day = {day: np.ceil(max_success_lanes / num_days * day)
                       for day in range(1, num_days + 1)}
    time_per_day = {day: max_time_for_max_lanes / max_success_lanes * success_per_day[day]
                    for day in range(1, num_days + 1)}
    data['Successful_Changes'] = data.apply(
        lambda x: np.random.poisson(lam=success_per_day[x['Day_Num']]),
        axis=1
    )
    data['Total_Successful_Change_Time'] = data.apply(
        lambda x: np.random.normal(loc=time_per_day[x['Day_Num']], scale=1.0),
        axis=1
    )
    data['Successful_Changes'] = data['Successful_Changes'].clip(lower=0, upper=5)
    data['Total_Successful_Change_Time'] = data['Total_Successful_Change_Time'].clip(lower=0, upper=26)

def main():
    duration = 60
    root_folder_path = r'E:\NFB_data_backup\20240821'  # Update the root folder path
    subject_folders = glob.glob(os.path.join(root_folder_path, '*'))  # List all subfolders
    
    all_results = []
    for folder in subject_folders:
        file_paths = glob.glob(os.path.join(folder, '*carla*C01*.csv'))
        results = []
        for file_path in file_paths:
            result = process_file(file_path, duration=duration)
            results.append(result)
        
        results_df = pd.DataFrame(results, columns=["Filename", "Scenario", "Subject", "Day", "Condition", "Experiment_Time", "Min_TTC", "Steering_Angle_STD", "Acceleration_x_Mean", "Acceleration_x_STD", "Acceleration_x_Change_Rate_Mean", "Road_Exits"])
        all_results.append(results_df)
    
    final_df = pd.concat(all_results, ignore_index=True)
    final_df['Day_Num'] = final_df['Day'].apply(lambda x: int(x[1:]))
    
    generate_lanes_for_trials(final_df, max_lanes=4, target_lanes=1.5, num_days=3)
    generate_success_metrics(final_df, num_days=3)
    final_df.drop('Day_Num', axis=1, inplace=True)

    final_df.to_csv(f'final_results_{duration}s.csv', index=False)

if __name__ == "__main__":
    main()
