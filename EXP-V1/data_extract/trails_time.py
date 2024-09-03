import pandas as pd
import numpy as np

file_path = r'D:\gitee\EEG_Neurofeedback\merged_results.csv'
data = pd.read_csv(file_path)

data['Day_Num'] = data['Day'].apply(lambda x: int(x[1:]))

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

generate_lanes_for_trials(data, max_lanes=4, target_lanes=1.5, num_days=3)
generate_success_metrics(data, num_days=3)

print(data[['Subject', 'Day', 'Average_Lanes_Per_Change', 'Successful_Changes', 'Total_Successful_Change_Time']].head())

data.to_csv('d.csv', index=False)
