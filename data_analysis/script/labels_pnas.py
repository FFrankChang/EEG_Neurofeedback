import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch, butter, filtfilt
import csv
import os

# Parameters
file_path = r'E:\Faller_et_al_2019_PNAS_EEG_Neurofeedback_VR_Flight\S05_F_CL_Sil_50_100_merged.csv'
event_file_path = r'E:\Faller_et_al_2019_PNAS_EEG_Neurofeedback_VR_Flight\S05_F_CL_Sil_50_100_event.csv'
base_dir = os.path.dirname(file_path)
output_dir = os.path.join(base_dir, 'Processed_PSD')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, 'test2.csv')
sfreq = 256
window_size = 256
step_size = 25
channels = ['F7', 'F8', 'P7', 'P8']

# Read data
data = pd.read_csv(file_path)

# Read event data and process timestamps
event_data = pd.read_csv(event_file_path)
# Filter event data
filtered_events = event_data[event_data['type'] == 'QRS-F_CL_Sil_50_100']
# Convert event timestamps from units to ms
filtered_events['Timestamp_ms'] = filtered_events['latency'] / 0.256

# Bandpass filter function
def bandpass_filter(data_segment, lowcut=1.0, highcut=40.0, fs=sfreq, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data_segment, axis=0)
    return y

# Frequency bands
bands = {
    'delta': (1, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (13, 30)
}

# Compute and save
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    header = ['time'] + [f'{ch}_{band}' for ch in channels for band in bands.keys()] + ['arousal_pl']
    writer.writerow(header)

    for start in range(0, len(data) - window_size + 1, step_size):
        end = start + window_size
        window_data = data.loc[start:end-1, channels]
        filtered_data = bandpass_filter(window_data.values)
        timestamp = data.iloc[end - 1]['time']
        row = [timestamp]

        channel_psd_sums = {band: [] for band in bands}
        for ch_data in filtered_data.T:
            f, psd = welch(ch_data, fs=sfreq, nperseg=256, window='hamming')
            for band, (low, high) in bands.items():
                band_psd = np.mean(psd[(f >= low) & (f <= high)])
                channel_psd_sums[band].append(band_psd)
                row.append(band_psd)

        arousal_pl = (np.mean(channel_psd_sums['alpha']) + np.mean(channel_psd_sums['beta'])) / \
                     (np.mean(channel_psd_sums['theta']) + np.mean(channel_psd_sums['delta']))
        row.append(arousal_pl)
        
        writer.writerow(row)

# Load and visualize data
raw_data = pd.read_csv(output_file)
smoothed_arousal = raw_data['arousal_pl'].rolling(window=10, center=True).mean()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(raw_data['time']/1000, raw_data['arousal_pl'], label='Raw Arousal', linewidth=0.5, alpha=0.5)
ax1.plot(raw_data['time']/1000, smoothed_arousal, label='Smoothed Arousal', linewidth=1.5, color='lightcoral')

# Plot event markers
for event_time in filtered_events['Timestamp_ms']:
    ax1.axvline(x=event_time/1000, color='blue', linestyle='--', alpha=0.7)  # Event times are also converted to seconds

ax1.set_xlabel('Timestamp (s)')
ax1.set_ylabel('Arousal Value')
ax1.set_title('Arousal Values with Smoothing and Event Markers')
plt.legend()
plt.show()
