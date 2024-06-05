import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import os
class DataManager:
    def __init__(self,data_dir):
        self.data_dir = data_dir
        self.folder_name =  os.path.basename(data_dir)
        self.freq = 1000
        self.eye_data = None
        self.carla_data = None
        self.eeg_data = None
        self.ecg_data = None
        self.heart_rate_data = None
        self.mode_times = []
        self.collision_times = []

    def load_eye_data(self, file_path):
        """Loads and processes eye-tracking data."""
        df = pd.read_csv(file_path)
        df['timestamp'] = df['StorageTime'] / 10000000
        storage_time_index = df.columns.get_loc('StorageTime')
        df.insert(storage_time_index, 'new_timestamp', df['timestamp'])
        df.drop(columns=['StorageTime', 'timestamp', 'ID'], inplace=True)
        df.rename(columns={'new_timestamp': 'timestamp'}, inplace=True)
        self.eye_data = df
        if self.data_ready():
            self.trim_data()

    def load_carla_data(self, file_path):
        """Loads and processes Carla simulation data."""
        self.carla_data = pd.read_csv(file_path)
        self.carla_data = self.split_steer_column(self.carla_data)
        self.calculate_ttc(self.carla_data)
        self.load_event_data()
        if self.data_ready():
            self.trim_data()

    def load_eeg_data(self, file_path):
        """Loads EEG data and computes additional arousal columns."""
        self.eeg_data = pd.read_csv(file_path)
        if 'F7_alpha' in self.eeg_data.columns:
            for channel in ['F7', 'F8', 'P7', 'P8']:
                alpha_col = f'{channel}_alpha'
                beta_col = f'{channel}_beta'
                theta_col = f'{channel}_theta'
                delta_col = f'{channel}_delta'
                self.eeg_data[f'{channel}_arousal'] = (self.eeg_data[alpha_col] + self.eeg_data[beta_col]) / (self.eeg_data[theta_col] + self.eeg_data[delta_col])
        if self.data_ready():
            self.trim_data()

    def load_ecg_data(self, file_path):
        """Loads and processes ECG data."""
        self.ecg_data = pd.read_csv(file_path)
        self.calculate_heart_rate()
        if self.data_ready():
            self.trim_data()

    def calculate_heart_rate(self):
        """Calculates heart rate from ECG data."""
        ecg_values = self.ecg_data['BIP 01'].values
        peaks, _ = find_peaks(ecg_values, distance=self.freq / 2)
        rr_intervals = np.diff(peaks) / self.freq
        heart_rate = 60 / rr_intervals
        heart_rate_times = self.ecg_data['timestamp'].iloc[peaks][1:]  # Skipping the first peak
        self.heart_rate_data = pd.DataFrame({'timestamp': heart_rate_times, 'heart_rate': heart_rate})

    def data_ready(self):
        """Checks if all necessary datasets are loaded for synchronization."""
        return all(data is not None for data in [self.eye_data, self.carla_data, self.eeg_data, self.ecg_data])

    def trim_data(self):
        """Ensures all datasets have the same time range."""
        min_time = max(data['timestamp'].min() for data in [self.eye_data, self.carla_data, self.eeg_data, self.ecg_data] if data is not None)
        max_time = min(data['timestamp'].max() for data in [self.eye_data, self.carla_data, self.eeg_data, self.ecg_data] if data is not None)
        self.eye_data = self.eye_data[(self.eye_data['timestamp'] >= min_time) & (self.eye_data['timestamp'] <= max_time)]
        self.carla_data = self.carla_data[(self.carla_data['timestamp'] >= min_time) & (self.carla_data['timestamp'] <= max_time)]
        self.eeg_data = self.eeg_data[(self.eeg_data['timestamp'] >= min_time) & (self.eeg_data['timestamp'] <= max_time)]
        self.ecg_data = self.ecg_data[(self.ecg_data['timestamp'] >= min_time) & (self.ecg_data['timestamp'] <= max_time)]
        self.heart_rate_data = self.heart_rate_data[(self.heart_rate_data['timestamp'] >= min_time) & (self.heart_rate_data['timestamp'] <= max_time)]

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

    def load_event_data(self):
        """Load mode switch and collision events from carla_data."""
        if self.carla_data is not None:
            event_data = self.carla_data.copy()
            event_data['timestamp'] = pd.to_datetime(event_data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
            self.mode_times = event_data[event_data['Mode_Switched'] == 'Yes']['timestamp'].tolist()
            self.collision_times = event_data[event_data['Collision'] == 'Yes']['timestamp'].tolist()

    def sync_data(self):
        """Synchronizes data by merging datasets on their timestamps."""
        if not self.data_ready():
            raise ValueError("Not all data types are loaded.")
        datasets = [self.eye_data, self.carla_data, self.eeg_data, self.heart_rate_data]
        merged_data = datasets[0]
        for data in datasets[1:]:
            if data is not None:
                merged_data = pd.merge(merged_data, data, on='timestamp', how='outer')
        return merged_data
