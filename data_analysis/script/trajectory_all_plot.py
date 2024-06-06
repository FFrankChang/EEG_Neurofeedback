import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def plot_trajectories(folder_paths, subject=None,scenario=None,output_path=None):
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, 10)) 
    color_idx = 0 
    for folder_path in folder_paths:
        for file in os.listdir(folder_path):
            if 'carla' in file and file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    data = pd.read_csv(file_path)
                    ax.plot(data['Location_x'], data['Location_y'], label=os.path.basename(folder_path), color=colors[color_idx % 10])
                    color_idx += 1

    for line in [2992.5, 2996.25, 3000, 3003.75, 3007.5, 3011.25]:
        ax.axhline(y=line, color='grey', linestyle='-', linewidth=0.5)
    ax.set_xlim(5500,3000)
    ax.set_ylim(2970,3030)
    ax.set_xlabel('Location X')
    ax.set_ylabel('Location Y')
    ax.legend()
    plt.title(f'{subject}_{scenario}', fontweight='bold')
    if output_path:
        plt.savefig(os.path.join(output_path, f'{subject}_{scenario}_trajectory.png'))
    plt.show()
    plt.close(fig)
    

csv_file_path = r'D:\gitee\EEG_Neurofeedback\data\trails_index.csv'

for i in range(5,11):
    subject = 's'+ str(i).zfill(2)
    pic_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\trajectory'
    # print(subject)
    hard_files = filter_folder_paths(csv_file_path,subject=subject,scenario='hard')
    easy_files = filter_folder_paths(csv_file_path,subject=subject,scenario='easy')
    plot_trajectories(easy_files,subject=subject,scenario='easy')#,output_path=pic_path)
    plot_trajectories(hard_files,subject=subject,scenario='hard')#,output_path=pic_path)
