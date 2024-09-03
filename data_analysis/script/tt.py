import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, filtfilt

# Load the data
file_path = r'D:\gitee\EEG_Neurofeedback\data\20240523_s03_11_hard_feedback\eegraw_20240523_202718_final.csv'
data = pd.read_csv(file_path)
ecg_signal = data['BIP 01']

# High-pass filter
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Apply the filter
filtered_signal = highpass_filter(ecg_signal, cutoff=0.5, fs=1000)  # Cutoff frequency in Hz
print(filtered_signal)
# Convert sample indices to time in seconds
data['Time (s)'] = data.index / 1000
print(data['Time (s)'])
# Plotting
plt.figure(figsize=(12, 6))
plt.plot(data['Time (s)'][:5000], filtered_signal[:5000], label='Filtered BIP 01')
plt.title('Time Series Plot of Filtered BIP 01')
plt.xlabel('Time (s)')
plt.ylabel('BIP 01')
plt.grid(True)
plt.legend()
plt.show()
