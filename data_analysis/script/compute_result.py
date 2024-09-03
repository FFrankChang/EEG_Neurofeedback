import pandas as pd
import os

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

class DataProcessor:
    def __init__(self, subject, file_paths):
        self.subject = subject
        self.carla_data = None
        self.deceleration_periods = []
        self.file_paths = file_paths
        columns = ["subject", "experiment_no", "scenario", "condition", "deceleration_index", "Steering_Angle_Std"]
        self.results_df = pd.DataFrame(columns=columns)

    def process_folders(self):

        for path in self.file_paths:
            file_path = os.path.join(path, "carla_merged.csv")
            folder_name = os.path.basename(path)
            if os.path.exists(file_path):
                self.carla_data = pd.read_csv(file_path)
                self.detect_deceleration_periods()
                self.calculate_statistics(folder_name)

    def detect_deceleration_periods(self):
        """Detects continuous deceleration periods based on speed thresholds."""
        self.carla_data['Mode_Switched'] = self.carla_data['Mode_Switched'].fillna("No")
        switch_indices = self.carla_data.index[self.carla_data['Mode_Switched'].eq("Yes")]
        temp_periods = []
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
                        end_time = subset['timestamp'][i-1]+3
                        temp_periods.append((start_time, end_time))
            if in_deceleration and start_time:
                end_time = subset['timestamp'].iloc[-1]+3
                temp_periods.append((start_time, end_time))

        if temp_periods:
            merged_periods = [temp_periods[0]]
            for start, end in temp_periods[1:]:
                last_end = merged_periods[-1][1]
                if start - last_end <= 0.5:
                    merged_periods[-1] = (merged_periods[-1][0], end)
                else:
                    merged_periods.append((start, end))
            self.deceleration_periods = merged_periods[:5]  # Limit to the first five periods

    def calculate_statistics(self, folder):
        # Extract experiment number correctly
        experiment_no = folder.split('_')[2]
        scenario = 'easy' if 'easy' in folder.lower() else 'hard'
        condition = 'silence' if 'silence' in folder.lower() else 'feedback'
        
        for idx, (start, end) in enumerate(self.deceleration_periods, start=1):
            deceleration_data = self.carla_data[(self.carla_data['timestamp'] >= start) & (self.carla_data['timestamp'] <= end)]
            steering_angle_std = deceleration_data['Steering_Angle'].std() if not deceleration_data.empty else 0
            # Append results to DataFrame with deceleration index
            self.results_df = self.results_df.append({
                "subject": self.subject,
                "experiment_no": experiment_no,
                "scenario": scenario,
                "condition": condition,
                "deceleration_index": idx,
                "Steering_Angle_Std": steering_angle_std
            }, ignore_index=True)

    def save_results(self):
        self.results_df.to_csv(f"./data/{self.subject}_results_allthetime.csv", index=False)

index_csv_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv'
for i in range(1,11):
    subject = 's'+ str(i).zfill(2)
    folder_paths=filter_folder_paths(index_csv_path,subject=subject)
    processor = DataProcessor(subject,folder_paths)
    processor.process_folders()
    processor.save_results()
