import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt
from datetime import datetime
import os
import csv

def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=250, order=4):  # Example sampling rate (fs)
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def process_eeg_data(file_path, selected_channels, window_size=1000, step_size=100, sfreq=250):
    data = pd.read_csv(file_path)
    processed_data = []
    samples = [np.zeros(len(selected_channels)) for _ in range(window_size)]
    for index in range(0, len(data), step_size):
        window_data = data.iloc[index:index+window_size]
        if len(window_data) < window_size:
            continue
        filtered_samples = np.array([bandpass_filter(window_data[ch].values, fs=sfreq) for ch in selected_channels])
        f, psd = welch(filtered_samples, fs=sfreq, nperseg=500, window='hamming')
        result_row = [window_data['timestamp'].iloc[-1]]  # Use last timestamp in window
        for i, ch in enumerate(selected_channels):
            band_psds = [np.mean(psd[i, (f >= low) & (f <= high)]) for low, high in bands.values()]
            result_row.extend(band_psds)
        arousal = sum(band_psds[2] for _ in selected_channels) / sum(band_psds[1] for _ in selected_channels)
        result_row.append(arousal)
        processed_data.append(result_row)
    
    # Save processed data to CSV
    header = ['timestamp'] + [f'{ch}_{band}' for ch in selected_channels for band in bands.keys()] + ['arousal']
    with open('processed_eeg_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(processed_data)

# Configuration
bands = {
    'delta': (1, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (15, 30)
}
selected_channels = ['C3', 'C4', 'F3', 'F4']
file_path = r'E:\EEG_Neurofeedback\data\20240528_yh_11_hard(silence)\eegraw_20240528_151425_final.csv'

# Run processing
process_eeg_data(file_path, selected_channels)
