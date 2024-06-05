import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# Load your data
file_path = r'D:\gitee\EEG_Neurofeedback\data\test\20240531_lxk_05_easy_silence\carla_merged.csv'
data = pd.read_csv(file_path)

# Assume arousal data is in a column named 'Arousal' in the same CSV
arousal = data['arousal'].astype(float)

TTC_numeric = data['TTC'].astype(float)
TTC_numeric = np.log1p(TTC_numeric)

mode_switched_points = data[data['Mode_Switched'] == 'Yes']
collision_points = data[data['Collision'] == 'Yes']

# Create a figure with a GridSpec that makes room for a colorbar
fig = plt.figure(figsize=(14, 12))
gs = gridspec.GridSpec(2, 2, width_ratios=[20, 1], height_ratios=[3, 1])

# Plot the trajectory in a larger subplot
ax1 = fig.add_subplot(gs[0, 0])
sc = ax1.scatter(data['Location_x'], data['Location_y'], c=TTC_numeric, cmap='viridis', s=5, edgecolor='none', alpha=0.5)
ax1.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'], facecolors='none', edgecolors='b', s=50, label='Take Over')
ax1.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='red', s=50, label='Collision')

# Add horizontal lines for reference
ax1.axhline(y=3000, color='grey', linestyle='-', linewidth=0.5)
ax1.axhline(y=3003.75, color='grey', linestyle='-', linewidth=0.5)
ax1.axhline(y=3007.5, color='grey', linestyle='-', linewidth=0.5)
ax1.axhline(y=3011.25, color='grey', linestyle='-', linewidth=0.5)
ax1.axhline(y=2996.25, color='grey', linestyle='-', linewidth=0.5)
ax1.axhline(y=2992.5, color='grey', linestyle='-', linewidth=0.5)

ax1.set_aspect('equal')
ax1.set_ylabel('Location Y')
# ax1.legend()
ax1.set_title('Dynamic Color Vehicle Trajectory Based on TTC')
ax1.set_xlim(3000, 5000)
ax1.invert_xaxis()
# Add a colorbar in its own subplot, adjust if necessary
cbar_ax = fig.add_subplot(gs[0, 1])
fig.colorbar(sc, cax=cbar_ax, label='TTC')

# Plot the arousal on the second row, taking both columns
ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(data['Location_x'], arousal, label='Arousal', color='lightcoral')
ax2.set_ylabel('Arousal')
ax2.set_xlabel('Location X')
ax2.set_xlim(3000, 5000)
ax2.invert_xaxis()
# Ensure tight layout to align axes properly
plt.tight_layout()

# Display the plot
plt.show()
