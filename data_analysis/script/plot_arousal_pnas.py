import pandas as pd
import matplotlib.pyplot as plt

# Load data
raw_data_path = r'E:\EEG_Neurofeedback\test2.csv'
raw_data = pd.read_csv(raw_data_path)

# Filter the data
filtered_data = raw_data[(raw_data['time']/1000 >= 700) & (raw_data['time']/1000 <= 750)]

# Calculate the moving average
smoothed_arousal = filtered_data['arousal_pl'].rolling(window=10, center=True).mean()

# Create the plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot raw arousal values
ax1.plot(filtered_data['time']/1000, filtered_data['arousal_pl'], label='Raw Arousal', linewidth=0.5, alpha=0.5)

# Plot smoothed arousal values
ax1.plot(filtered_data['time']/1000, smoothed_arousal, label='Smoothed Arousal', linewidth=1.5, color='lightcoral')

ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Arousal Value')
ax1.set_title('Arousal Values Between 750 and 800 Seconds with Smoothing')
plt.legend()
plt.show()