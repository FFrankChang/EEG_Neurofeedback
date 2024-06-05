import pandas as pd
import numpy as np
import os

def split_steer_column(data):
    """拆分Steer列到三个新列：Steering_Angle, Throttle, Brake"""
    data['Steer'] = data['Steer'].apply(eval)
    data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0])
    data['Throttle'] = data['Steer'].apply(lambda x: x[1])
    data['Brake'] = data['Steer'].apply(lambda x: x[2])
    data.drop('Steer', axis=1, inplace=True)
    return data

def calculate_ttc(data):
    """计算TTC并更新数据"""
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

def process_folder(directory):
    for root, dirs, files in os.walk(directory):
        if 'sj' in root :
            carla_files = [f for f in files if 'carla' in f]
            psd_files = [f for f in files if 'psd' in f]
            for carla_file, psd_file in zip(carla_files, psd_files):
                carla_path = os.path.join(root, carla_file)
                psd_path = r'D:\gitee\EEG_Neurofeedback\data\normalized_arousal_sj.csv'
                output_path = os.path.join(root, 'carla_merged.csv')
                merge_datasets(carla_path, psd_path, output_path)

# 设置目录并处理文件
directory = r'D:\gitee\EEG_Neurofeedback\data'
process_folder(directory)
