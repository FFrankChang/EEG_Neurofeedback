import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and preprocess data
file_path = r'D:\gitee\EEG_Neurofeedback\data\test\20240531_lxk_05_easy_silence\carla_merged.csv'
data = pd.read_csv(file_path, dtype={'arousal': float, 'TTC': float})
data['TTC'] = np.log1p(data['TTC'])

# Points for special markers
mode_switched_points = data[data['Mode_Switched'] == 'Yes']
collision_points = data[data['Collision'] == 'Yes']

def plot_trajectory(ax, x, y, c, cmap, label, alpha=1, size=10):
    sc = ax.scatter(x, y, c=c, cmap=cmap, s=size, edgecolor='none', alpha=alpha)
    plt.colorbar(sc, ax=ax, label=label)
    ax.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'], facecolors='none', edgecolors='red', s=50, label='Take Over')
    ax.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='black', s=50, label='Collision')
    for line in [2992.5, 2996.25, 3000, 3003.75, 3007.5, 3011.25]:
        ax.axhline(y=line, color='grey', linestyle='-', linewidth=0.5)
    ax.set(xlabel='Location X', ylabel='Location Y')
    ax.legend()

# Create figure and axes
fig, axes = plt.subplots(1, 2, figsize=(18, 6))
plot_trajectory(axes[0], data['Location_x'], data['Location_y'], data['arousal'], 'binary', 'arousal', size=20)
plot_trajectory(axes[1], data['Location_x'], data['Location_y'], data['TTC'], 'viridis', 'TTC', alpha=0.5, size=10)

axes[0].set_title('Dynamic Color Vehicle Trajectory Based on Arousal')
axes[1].set_title('Dynamic Color Vehicle Trajectory Based on TTC')

plt.show()
