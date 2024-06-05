import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 定义绘图函数
def plot_trajectory(ax, x, y, c, cmap, label, alpha=1, size=10):
    sc = ax.scatter(x, y, c=c, cmap=cmap, s=size, edgecolor='none', alpha=alpha)
    plt.colorbar(sc, ax=ax, label=label)
    global mode_switched_points,collision_points
    ax.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'], facecolors='none', edgecolors='red', s=50, label='Take Over')
    ax.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='black', s=50, label='Collision')
    for line in [2992.5, 2996.25, 3000, 3003.75, 3007.5, 3011.25]:
        ax.axhline(y=line, color='grey', linestyle='-', linewidth=0.5)
    ax.set(xlabel='Location X', ylabel='Location Y')
    ax.legend()

# 主处理函数
def process_files(base_path):
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if 'carla_merged' in file and file.endswith('.csv'):
                    file_path = os.path.join(folder_path, file)
                    data = pd.read_csv(file_path, dtype={'arousal': float, 'TTC': float})
                    data['TTC'] = np.log1p(data['TTC'])
                    
                    global mode_switched_points,collision_points
                    mode_switched_points = data[data['Mode_Switched'] == 'Yes']
                    collision_points = data[data['Collision'] == 'Yes']
                    
                    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
                    plot_trajectory(axes[0], data['Location_x'], data['Location_y'], data['normalized_arousal'], 'binary', 'arousal', size=20)
                    plot_trajectory(axes[1], data['Location_x'], data['Location_y'], data['TTC'], 'viridis', 'TTC', alpha=0.5, size=10)

                    axes[0].set_title('Dynamic Color Vehicle Trajectory Based on Arousal')
                    axes[1].set_title('Dynamic Color Vehicle Trajectory Based on TTC')
                    
                    plt.savefig(os.path.join(folder_path, folder + '.png'))
                    output_path = r'D:\gitee\EEG_Neurofeedback\pic'
                    plt.savefig(f"{output_path}/{folder}.png")
                    plt.close(fig)  # 关闭图形以释放内存

# 设置基本路径
base_path = r'D:\gitee\EEG_Neurofeedback\data'
process_files(base_path)
