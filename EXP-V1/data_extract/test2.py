import pandas as pd
import numpy as np
import os

def split_steer_column(data):
    """拆分Steer列到三个新列：Steering_Angle, Throttle, Brake"""
    data['Steer'] = data['Steer'].apply(lambda x: eval(x))
    data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0]*540)
    data['Throttle'] = data['Steer'].apply(lambda x: x[1])
    data['Brake'] = data['Steer'].apply(lambda x: x[2])
    data.drop('Steer', axis=1, inplace=True)
    return data

def calculate_ttc(data):
    """计算TTC并更新data"""
    data['Distance'] = np.sqrt((data['Location_x'] - data['Lead_Vehicle_X'])**2 +
                               (data['Location_y'] - data['Lead_Vehicle_Y'])**2 +
                               (data['Location_z'] - data['Lead_Vehicle_Z'])**2)
    data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed'])
    data['TTC'] = data['Distance'] / data['Relative_Speed'].replace(0, np.inf)
    return data

def calculate_road_exits(data):
    """计算车辆离开道路的次数"""
    data['On_Road'] = (data['Location_y'] >= 2992.5) & (data['Location_y'] <= 3000)
    transitions = data['On_Road'].astype(int).diff().ne(0)
    road_exits = ((transitions) & (data['On_Road'].shift(-1) == False)).sum()
    return road_exits

def main():
    file_path = r'E:\NFB_data_backup\filtered\S08_D03\carla_C01_S08_D03_feedback_20240721162052.csv'
    filename = os.path.basename(file_path)
    data = pd.read_csv(file_path)
    
    data = split_steer_column(data)
    data = calculate_ttc(data)
    road_exits = calculate_road_exits(data)
    
    first_yes_index = data[data['TOR'] == 'Yes'].index[0]
    data_post_tor_yes = data.loc[first_yes_index:]
    min_ttc = data_post_tor_yes['TTC'].min()
    steering_angle_std = data_post_tor_yes['Steering_Angle'].std()
    acceleration_x_mean = data_post_tor_yes['Acceleration_x'].mean()
    acceleration_x_std = data_post_tor_yes['Acceleration_x'].std()
    data_post_tor_yes['Acceleration_x_change_rate'] = data_post_tor_yes['Acceleration_x'].diff() / data_post_tor_yes['timestamp'].diff()
    acceleration_x_change_rate_mean = data_post_tor_yes['Acceleration_x_change_rate'].mean()

    results = pd.DataFrame({
        "Filename": [filename],
        "Min_TTC": [min_ttc],
        "Steering_Angle_STD": [steering_angle_std],
        "Acceleration_x_Mean": [acceleration_x_mean],
        "Acceleration_x_STD": [acceleration_x_std],
        "Acceleration_x_Change_Rate_Mean": [acceleration_x_change_rate_mean],
        "Road_Exits": [road_exits]
    })
    
    results.to_csv('processed_data_results.csv', index=False)

    return data_post_tor_yes

if __name__ == "__main__":
    resulting_data = main()
