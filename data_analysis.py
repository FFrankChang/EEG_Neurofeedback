import pandas as pd
import numpy as np
import os

class DataManager:
    def __init__(self, eye_csv_path, carla_csv_path, eeg_csv_path):
        self.eye_data = self.load_and_process_eye_data(eye_csv_path)
        self.carla_data = self.load_and_process_carla_data(carla_csv_path)
        self.eeg_data = self.load_csv_data(eeg_csv_path, skiprows=0)
        self.trim_data()
        self.load_event_data()
        self.sync_data = self.sync_data()
        
    def load_csv_data(self, file_path, skiprows=None):
        """加载CSV文件数据"""
        return pd.read_csv(file_path, skiprows=skiprows)

    def load_and_process_eye_data(self, file_path):
        """读取并处理眼动数据，调整时间戳格式并调整列位置"""
        df = pd.read_csv(file_path)
        df['timestamp'] = df['StorageTime'] / 10000000
        storage_time_index = df.columns.get_loc('StorageTime')
        df.insert(storage_time_index, 'new_timestamp', df['timestamp'])
        df.drop(columns=['StorageTime', 'timestamp','ID'], inplace=True)
        df.rename(columns={'new_timestamp': 'timestamp'}, inplace=True)
        
        return df
    
    def load_event_data(self):
        """Load mode switch and collision events."""
        event_data = self.carla_data
        self.mode_times = event_data[event_data['Mode_Switched'] == 'Yes']['timestamp'].tolist()
        self.collision_times = event_data[event_data['Collision'] == 'Yes']['timestamp'].tolist()
        
    def load_and_process_carla_data(self, file_path):
        """加载并处理Carla数据，包括拆分Steer列和计算TTC"""
        data = pd.read_csv(file_path)
        data = self.split_steer_column(data)
        self.calculate_ttc(data)
        return data

    def split_steer_column(self, data):
        """拆分Steer列到三个新列：Steering_Angle, Throttle, Brake"""
        data['Steer'] = data['Steer'].apply(lambda x: eval(x))
        data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0])
        data['Throttle'] = data['Steer'].apply(lambda x: x[1])
        data['Brake'] = data['Steer'].apply(lambda x: x[2])
        data.drop('Steer', axis=1, inplace=True)
        return data

    def calculate_ttc(self, data):
        """计算TTC并更新carla_data"""
        data['Distance'] = np.sqrt((data['Location_x'] - data['Lead_Vehicle_X'])**2 +
                                   (data['Location_y'] - data['Lead_Vehicle_Y'])**2 +
                                   (data['Location_z'] - data['Lead_Vehicle_Z'])**2)
        data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed'])
        data['TTC'] = data['Distance'] / data['Relative_Speed'].replace(0, np.inf)
        self.carla_data = data

    def save_data(self, data, filename):
        """保存数据到CSV文件"""
        # output_file_path = os.path.join(self.output_directory, filename)
        data.to_csv(filename, index=False)
        return filename

    def trim_data(self):
        """修剪数据以确保所有数据集具有相同的时间范围"""
        start_time = max(self.eye_data['timestamp'].min(), self.carla_data['timestamp'].min(), self.eeg_data['timestamp'].min())
        end_time = min(self.eye_data['timestamp'].max(), self.carla_data['timestamp'].max(), self.eeg_data['timestamp'].max())
        self.eye_data = self.eye_data[(self.eye_data['timestamp'] >= start_time) & (self.eye_data['timestamp'] <= end_time)]
        self.carla_data = self.carla_data[(self.carla_data['timestamp'] >= start_time) & (self.carla_data['timestamp'] <= end_time)]
        self.eeg_data = self.eeg_data[(self.eeg_data['timestamp'] >= start_time) & (self.eeg_data['timestamp'] <= end_time)]
        
    def sync_data(self):
        
        merged_data = pd.merge(self.eye_data, self.carla_data, on='timestamp',how='outer')
        merged_data = pd.merge(merged_data, self.eeg_data, on='timestamp',how='outer')

        return merged_data
