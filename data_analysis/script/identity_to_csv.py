import pandas as pd
import os

class VehicleDataProcessor:
    def __init__(self, file_path):
        self.carla_data = pd.read_csv(file_path)
        self.events = []
        self.last_event_time = None  # 追踪上一次事件的时间

    def fill_missing_values(self):
        """Fill missing values in the 'Mode_Switched' column."""
        self.carla_data['Mode_Switched'] = self.carla_data['Mode_Switched'].fillna("No")

    def detect_events(self):
        """Detects Mode_Switched to Yes events and continuous deceleration periods."""
        self.fill_missing_values()
        switch_indices = self.carla_data.index[self.carla_data['Mode_Switched'].eq("Yes")].tolist()

        # Record Mode_Switched to Yes events
        for idx in switch_indices:
            timestamp = self.carla_data.loc[idx, 'timestamp']
            self.events.append({'timestamp': timestamp, 'Event_Type': 'take-over'})

        # Detect deceleration periods
        for index in switch_indices:
            subset = self.carla_data.loc[index:].reset_index(drop=True)
            speed_less_than_75 = subset['Lead_Vehicle_Speed'] < 75
            in_deceleration = False
            start_time = None
            
            for i, (time, speed, is_below_threshold) in enumerate(zip(subset['timestamp'], subset['Lead_Vehicle_Speed'], speed_less_than_75)):
                if is_below_threshold and not in_deceleration:
                    in_deceleration = True
                    start_time = time
                elif not is_below_threshold and in_deceleration:
                    in_deceleration = False
                    if start_time:
                        if not self.last_event_time or (start_time - self.last_event_time >= 3):
                            self.events.append({'timestamp': start_time, 'Event_Type': 'event'})
                            self.last_event_time = start_time
                        start_time = None

    def save_events_to_csv(self, output_file):
        """Saves the detected events to a CSV file."""
        if self.events:
            df = pd.DataFrame(self.events)
            df.to_csv(output_file, index=False)
        else:
            print("No events detected.")

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

index_csv_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv'
folder_paths=filter_folder_paths(index_csv_path,subject='s10')

for path in folder_paths:
    file_path = os.path.join(path, 'carla_merged.csv')
    output_file = os.path.join(path, 'event.csv')
    processor = VehicleDataProcessor(file_path)
    processor.detect_events()
    processor.save_events_to_csv(output_file)
