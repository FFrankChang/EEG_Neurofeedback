import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import os  # Import os to extract the folder name


def plot_save(file_path):
    
    data = pd.read_csv(file_path, dtype={'arousal': float, 'TTC': float})
    data['TTC'] = np.log1p(data['TTC'])

    mode_switched_points = data[data['Mode_Switched'] == 'Yes']
    collision_points = data[data['Collision'] == 'Yes']

    def plot_trajectory(ax, x, y, c, cmap, label, alpha=1, size=10):
        sc = ax.scatter(x, y, c=c, cmap=cmap, s=size, edgecolor='none', alpha=alpha)
        plt.colorbar(sc, ax=ax, label=label)
        ax.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'], facecolors='none', edgecolors='blue', s=50, label='Take Over')
        ax.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='red', s=50, label='Collision')
        for line in [2992.5, 2996.25, 3000, 3003.75, 3007.5, 3011.25]:
            ax.axhline(y=line, color='grey', linestyle='-', linewidth=0.5)
        ax.set_xlim(5500,3000)
        ax.set_ylim(2970,3030)
        ax.set(xlabel='Location X', ylabel='Location Y')
        ax.legend()

    # Extract folder name from the file path for the overall title
    folder_name = os.path.basename(os.path.dirname(file_path))

    # Create figure and axes
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    plot_trajectory(axes[0], data['Location_x'], data['Location_y'], data['arousal'], 'binary', 'arousal', size=20)
    plot_trajectory(axes[1], data['Location_x'], data['Location_y'], data['TTC'], 'viridis', 'TTC', alpha=0.5, size=10)

    axes[0].set_title('Dynamic Color Vehicle Trajectory Based on Arousal')
    axes[1].set_title('Dynamic Color Vehicle Trajectory Based on TTC')

    # Set the overall title for the figure
    plt.suptitle(folder_name)
    save_path = os.path.join(r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\trajectory_arousal', f"{folder_name}_event_trajectory.png")
    plt.savefig(save_path)
    # plt.show()
    
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
folder_paths=filter_folder_paths(index_csv_path)

for path in folder_paths:
    file_path = os.path.join(path, 'carla_merged.csv')
    plot_save(file_path)