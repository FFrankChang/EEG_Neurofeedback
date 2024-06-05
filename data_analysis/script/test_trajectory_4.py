import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider

# Load your data
file_path = r'D:\gitee\EEG_Neurofeedback\data\test\20240531_lxk_05_easy_silence\carla_merged.csv'
data = pd.read_csv(file_path)

# Assume arousal data is in a column named 'Arousal' in the same CSV
arousal = data['arousal'].astype(float)

TTC_numeric = data['TTC'].astype(float)
TTC_numeric = np.log1p(TTC_numeric)

mode_switched_points = data[data['Mode_Switched'] == 'Yes']
collision_points = data[data['Collision'] == 'Yes']

# Create a figure with a GridSpec for layout management
fig = plt.figure(figsize=(14, 12))
gs = gridspec.GridSpec(3, 2, width_ratios=[20, 1], height_ratios=[1, 2, 1])

# Plot the trajectory
ax1 = fig.add_subplot(gs[0, 0])
sc = ax1.scatter(data['Location_x'], data['Location_y'], c=TTC_numeric, cmap='viridis', s=10, edgecolor='none', alpha=0.5)
ax1.scatter(mode_switched_points['Location_x'], mode_switched_points['Location_y'], facecolors='none', edgecolors='red', s=50, label='Take Over')
ax1.scatter(collision_points['Location_x'], collision_points['Location_y'], facecolors='none', edgecolors='black', s=50, label='Collision')

ax1.set_aspect('equal')
ax1.set_xlim(5500, 3000)  # Set fixed x-limits
ax1.set_ylabel('Location Y')
# ax1.legend()
ax1.set_title('Dynamic Color Vehicle Trajectory Based on TTC')

# Add a colorbar
cbar_ax = fig.add_subplot(gs[0, 1])
fig.colorbar(sc, cax=cbar_ax, label='TTC')

# Plot arousal data
ax2 = fig.add_subplot(gs[1, 0])
line, = ax2.plot(data['Location_x'], arousal, label='Arousal', color='blue')
ax2.set_xlim(5500, 3000)  # Set fixed x-limits
ax2.set_ylabel('Arousal')
ax2.set_xlabel('Location X')

# Create a slider
axcolor = 'lightgoldenrodyellow'
ax_slider = fig.add_subplot(gs[2, :])
slider = Slider(ax_slider, 'Start X', 3000, 5500, valinit=5500, valstep=1)

# Update function for the slider
def update(val):
    start_x = slider.val
    end_x = start_x - 500  # Show a fixed length of 500 units
    ax1.set_xlim(start_x, end_x)
    ax2.set_xlim(start_x, end_x)
    fig.canvas.draw_idle()

slider.on_changed(update)

# Ensure tight layout to align axes properly
plt.tight_layout()

# Show the plot with the slider
plt.show()
