import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"G:\Exp_V0_data\data\S06\S06_C04_simple_20241022_213314.csv")
df['event_triggered'] = df['event_triggered'].astype(bool)
event_indices = df[df['event_triggered']].index

nrows = (len(event_indices) + 3) // 4  
fig, axes = plt.subplots(nrows=nrows, ncols=4, figsize=(20, 5 * nrows), constrained_layout=True)
axes = axes.flatten()

for i in range(len(event_indices) - 1):
    start_idx = event_indices[i]
    end_idx = event_indices[i + 1] - 1
    start_time = df.loc[start_idx, 'timestamp']
    df['time_since_event_start'] = (df['timestamp'] - start_time) 
    axes[i].plot(df.loc[start_idx:end_idx, 'time_since_event_start'], df.loc[start_idx:end_idx, 'steer_angle'])
    axes[i].set_title(f'Event: {i}')
    axes[i].set_xlabel('Time (s)')
    axes[i].set_ylabel('Steer Angle')
    axes[i].grid(True)

for j in range(i + 1, len(axes)):
    axes[j].axis('off')

plt.savefig('event_steering_angles_grid.png')
plt.close(fig)  
