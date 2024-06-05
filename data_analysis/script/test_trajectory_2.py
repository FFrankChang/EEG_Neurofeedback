import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = r'D:\gitee\EEG_Neurofeedback\data\test\20240531_lxk_05_easy_silence\carla_merged.csv'
data = pd.read_csv(file_path)

# Convert Compass data to numeric values for color mapping
arousal_numeric = data['arousal'].astype(float)

plt.figure(figsize=(18, 6))
plt.subplot(1,2,1)
sc = plt.scatter(data['Location_x'], data['Location_y'], c=arousal_numeric, cmap='binary', s=20, edgecolor='none')
plt.colorbar(sc, label='arousal')

mode_switched_points = data[data['Mode_Switched'] == 'Yes']
collision_points = data[data['Collision'] == 'Yes']

plt.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'],facecolors='none', edgecolors='red', s=50, label='Take Over')
plt.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='black', s=50, label='Collision')


plt.axhline(y=3000, color='grey', linestyle='--')
plt.axhline(y=3003.75, color='grey', linestyle='--')
plt.axhline(y=3007.5, color='grey', linestyle='--')
plt.axhline(y=3011.25, color='grey', linestyle='--')
plt.axhline(y=2996.25, color='grey', linestyle='--')
plt.axhline(y=2992.5, color='grey', linestyle='--')

plt.title('Dynamic Color Vehicle Trajectory Based on Arousal')
plt.xlabel('Location X')
plt.ylabel('Location Y')
plt.legend()

plt.subplot(1,2,2)
TTC_numeric = data['TTC'].astype(float)
TTC_numeric = np.log1p(TTC_numeric)
sc = plt.scatter(data['Location_x'], data['Location_y'], c=TTC_numeric, cmap='viridis', s=10, edgecolor='none',alpha=0.5)
plt.colorbar(sc, label='TTC')
plt.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'],facecolors='none', edgecolors='red', s=50, label='Take Over')
plt.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='black', s=50, label='Collision')

plt.axhline(y=3000, color='grey', linestyle='-',linewidth=0.5)
plt.axhline(y=3003.75, color='grey', linestyle='-',linewidth=0.5)
plt.axhline(y=3007.5, color='grey', linestyle='-',linewidth=0.5)
plt.axhline(y=3011.25, color='grey', linestyle='-',linewidth=0.5)
plt.axhline(y=2996.25, color='grey', linestyle='-',linewidth=0.5)
plt.axhline(y=2992.5, color='grey', linestyle='-',linewidth=0.5)

plt.title('Dynamic Color Vehicle Trajectory Based on TTC')
plt.xlabel('Location X')
plt.ylabel('Location Y')
plt.legend()
plt.show()
