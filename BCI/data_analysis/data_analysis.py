import pandas as pd
import numpy as np
import os

class DataManager:
    def __init__(self, eye_csv_path, carla_csv_path, eeg_csv_path, output_directory):
        self.output_directory = output_directory
        self.eye_data = self.load_and_process_eye_data(eye_csv_path)
        self.carla_data = self.load_csv_data(carla_csv_path)
        self.eeg_data = self.load_csv_data(eeg_csv_path)
        self.calculate_ttc(self.carla_data)
        self.trim_data()

    def load_csv_data(self, file_path):
        """加载CSV文件数据"""
        return pd.read_csv(file_path)

    def load_and_process_eye_data(self, file_path):
        """读取并处理眼动数据，调整时间戳格式"""
        df = pd.read_csv(file_path)
        df['timestamp'] = df['StorageTime'] / 10000000  # 转换StorageTime生成新的timestamp列
        return df

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
        output_file_path = os.path.join(self.output_directory, filename)
        data.to_csv(output_file_path, index=False)
        return output_file_path

    def trim_data(self):
        """修剪数据以确保所有数据集具有相同的时间范围"""
        start_time = max(self.eye_data['timestamp'].min(), self.carla_data['timestamp'].min(), self.eeg_data['timestamp'].min())
        end_time = min(self.eye_data['timestamp'].max(), self.carla_data['timestamp'].max(), self.eeg_data['timestamp'].max())
        self.eye_data = self.eye_data[(self.eye_data['timestamp'] >= start_time) & (self.eye_data['timestamp'] <= end_time)]
        self.carla_data = self.carla_data[(self.carla_data['timestamp'] >= start_time) & (self.carla_data['timestamp'] <= end_time)]
        self.eeg_data = self.eeg_data[(self.eeg_data['timestamp'] >= start_time) & (self.eeg_data['timestamp'] <= end_time)]

    def sync_data(self):
        """同步三个数据源的数据，简单以时间戳为基准进行同步"""
        data_frames = [self.eye_data.set_index('timestamp'), self.carla_data.set_index('timestamp'), self.eeg_data.set_index('timestamp')]
        synced_data = pd.concat(data_frames, axis=1, join='inner').reset_index()
        return synced_data
