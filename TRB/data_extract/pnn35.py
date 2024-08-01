import pandas as pd
import numpy as np
from scipy.signal import find_peaks, butter, filtfilt

# Function to filter ECG signal
def filter_ecg(signal, fs):
    nyquist = 0.5 * fs
    low = 1 / nyquist
    high = 30 / nyquist
    b, a = butter(1, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

# Function to calculate heart rate
def calculate_heart_rate(r_peaks, fs):
    rr_intervals = np.diff(r_peaks) / fs * 1000  # convert to milliseconds
    heart_rate = 60000 / np.mean(rr_intervals)  # calculate heart rate
    return heart_rate, rr_intervals

# Function to calculate HRV PNN35
def calculate_hrv_pnn35(rr_intervals):
    rr_diff = np.abs(np.diff(rr_intervals))
    pnn35 = np.sum(rr_diff > 35) / len(rr_diff) * 100  # percentage of differences > 35ms
    return pnn35

# Load ECG data
file_path = '/path/to/your/file.csv'  # Update this path to your actual file location
data = pd.read_csv(file_path)

# Constants
fs = 1000  # Sampling rate in Hz

# Filter the ECG signal
filtered_ecg = filter_ecg(data['BIP 01'].values, fs)

# Detect R-peaks
peaks, _ = find_peaks(filtered_ecg, height=np.mean(filtered_ecg) + 2 * np.std(filtered_ecg))

# Calculate heart rate
heart_rate, rr_intervals = calculate_heart_rate(peaks, fs)

# Calculate HRV PNN35
pnn35 = calculate_hrv_pnn35(rr_intervals)

# Print results
print("Calculated Heart Rate: {:.2f} beats/min".format(heart_rate))
print("HRV PNN35: {:.2f}%".format(pnn35))
