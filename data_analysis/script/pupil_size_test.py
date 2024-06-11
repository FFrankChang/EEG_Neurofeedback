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

def calculate_pupil_averages(deceleration_csv, eyetracking_csv):
    deceleration_data = pd.read_csv(deceleration_csv)
    eye_data = pd.read_csv(eyetracking_csv)
    eye_data['StorageTime'] = eye_data['StorageTime'] / 10000000
    deceleration_data['Left_Pupil_Average'] = pd.NA
    deceleration_data['Right_Pupil_Average'] = pd.NA

    for index, row in deceleration_data.iterrows():
        start_time = row['Start_Time']
        end_time = row['End_Time']
        mask = (eye_data['StorageTime'] >= start_time) & (eye_data['StorageTime'] <= end_time)
        filtered_data = eye_data[mask]
        left_avg = filtered_data['smarteye|LeftPupilDiameter'].mean()
        right_avg = filtered_data['smarteye|RightPupilDiameter'].mean()

        deceleration_data.at[index, 'Left_Pupil_Average'] = round(left_avg, 8)
        deceleration_data.at[index, 'Right_Pupil_Average'] = round(right_avg, 8)

    deceleration_data.to_csv(deceleration_csv, index=False)
    print(deceleration_csv,'finished')

def process_folders(folder_list_csv, **filter_kwargs):
    folders = filter_folder_paths(folder_list_csv, **filter_kwargs)
    for folder in folders:
        dec_file = os.path.join(folder, 'deceleration_periods.csv')
        eyetracking_files = [f for f in os.listdir(folder) if f.startswith('Entity_Recording') and f.endswith('.csv')]
        for eyetracking_file in eyetracking_files:
            eye_file = os.path.join(folder, eyetracking_file)
            calculate_pupil_averages(dec_file, eye_file)

# Example usage
folders_csv = r'D:\Frank_Project\EEG_Neurofeedback\data\trails_index.csv'
process_folders(folders_csv)
