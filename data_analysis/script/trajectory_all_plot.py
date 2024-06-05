import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_trajectories(base_path, output_path, subject, model):
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, 10)) 
    color_idx = 0  # 颜色索引

    # 遍历基本路径下的文件夹
    for folder in os.listdir(base_path):
        if subject in folder and model in folder:
            folder_path = os.path.join(base_path, folder)
            file_path = os.path.join(folder_path, 'carla_merged.csv')
            if os.path.isfile(file_path):
                data = pd.read_csv(file_path)
                ax.plot(data['Location_x'], data['Location_y'], label=folder, color=colors[color_idx % 20])
                color_idx += 1
                
    for line in [2992.5, 2996.25, 3000, 3003.75, 3007.5, 3011.25]:
        ax.axhline(y=line, color='grey', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Location X')
    ax.set_ylabel('Location Y')
    ax.legend(title='Folders')
    plt.savefig(os.path.join(output_path, f'{subject}_{model}.png'))
    plt.close(fig)  # 关闭图形以释放内存

# 设置基本路径和输出路径
base_path = r'D:\gitee\EEG_Neurofeedback\data'
output_path = r'D:\gitee\EEG_Neurofeedback\pic_all'
sub = 'zyx'
plot_trajectories(base_path, output_path,sub,'easy')
plot_trajectories(base_path, output_path,sub,'hard')
