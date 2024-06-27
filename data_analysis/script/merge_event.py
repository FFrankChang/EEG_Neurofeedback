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

def merge_eeg_raw_csv_files(folder_paths, output_csv_path):
    all_data = pd.DataFrame()
    for path in folder_paths:
        csv_files = glob.glob(os.path.join(path, '*eeg*.csv'))
        print(csv_files)
        for file in csv_files:
            df = pd.read_csv(file)
            all_data = pd.concat([all_data, df], ignore_index=True)
    all_data.to_csv(output_csv_path, index=False)



subject = 's09'
scenario = 'easy'
condition = 'silence'
index_csv_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv'
output_csv_path = rf'{subject}_{scenario}_{condition}.csv'

# 获取特定受试者的文件夹路径
folder_paths = filter_folder_paths(index_csv_path, subject=subject,scenario=scenario,condition=condition)

# 合并特定文件并保存
merge_eeg_raw_csv_files(folder_paths, output_csv_path)
