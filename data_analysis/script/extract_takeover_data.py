import pandas as pd
import os
import glob

def filter_folder_paths(csv_file_path, date=None, subject=None, experiment_no=None, scenario=None, condition=None):
    data = pd.read_csv(csv_file_path)
    if date:
        data = data[data['Date'] == date]
    if subject:
        data = data[data['Subject'] == subject]
    if experiment_no:
        data = data[data['ExperimentNo'] == experiment_no]
    if scenario:
        data = data[data['Scenario'] == scenario]
    if condition:
        data = data[data['Condition'] == condition]
    return data['FolderPath'].tolist()

class VehicleDataProcessor:
    def __init__(self, carla_file_path, eeg_file_path):
        self.carla_data = pd.read_csv(carla_file_path)
        self.eeg_data = pd.read_csv(eeg_file_path)
        self.first_takeover_time = None

    def fill_missing_values(self):
        """Fill missing values in the 'Mode_Switched' column."""
        self.carla_data['Mode_Switched'] = self.carla_data['Mode_Switched'].fillna("No")

    def find_first_takeover_event(self):
        """Finds the first time when Mode_Switched changed to Yes and returns its timestamp."""
        self.fill_missing_values()
        switch_indices = self.carla_data.index[self.carla_data['Mode_Switched'].eq("Yes")].tolist()
        if switch_indices:
            self.first_takeover_time = self.carla_data.loc[switch_indices[0], 'timestamp']

    def filter_eeg_data(self):
        """Filter out EEG data before the first takeover time."""
        if self.first_takeover_time:
            self.eeg_data = self.eeg_data[self.eeg_data['timestamp'] >= self.first_takeover_time]

    def save_filtered_eeg_data(self, output_file_path):
        """Saves the filtered EEG data to a new file."""
        if self.first_takeover_time:
            self.eeg_data.to_csv(output_file_path, index=False)
        else:
            print("No takeover event found. No data saved.")

def process_data_in_folder(folder_path):
    carla_file_path = os.path.join(folder_path, 'carla_merged.csv')
    eeg_file_paths = glob.glob(os.path.join(folder_path, '*eeg*.csv'))
    if not eeg_file_paths:
        print("No EEG files found in the directory.")
        return

    for eeg_file_path in eeg_file_paths:
        processor = VehicleDataProcessor(carla_file_path, eeg_file_path)
        processor.find_first_takeover_event()
        processor.filter_eeg_data()
        eeg_filename = os.path.basename(folder_path)
        
        output_file_path = f"{eeg_filename}_takeover.csv"
        processor.save_filtered_eeg_data(output_file_path)
        

index_csv_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv'
folder_paths=filter_folder_paths(index_csv_path,subject='s10')

for path in folder_paths:

    process_data_in_folder(path)
