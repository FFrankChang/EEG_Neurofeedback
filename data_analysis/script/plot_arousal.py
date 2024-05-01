import numpy as np
import pandas as pd
from scipy.signal import welch, butter, sosfiltfilt,filtfilt
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 参数设置
file_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\data\\20240430_01_final_02\\eegraw_20240430_152635_final.csv'  # 原始数据文件路径
output_file = 'processed_arousal_values.csv'  # 输出文件路径
sfreq = 1000  
window_size = 1000
step_size = 100
channels = ['F7', 'F8', 'P7', 'P8']  # 实时处理时使用的通道列表

# 读取数据
data = pd.read_csv(file_path)

# 带通滤波函数
def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=1000, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', output='sos')
    y = filtfilt(sos, data, axis=0)
    return y

filtered_data = bandpass_filter(data[channels].values)

# 设置频段
bands = {
    'delta': (1, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (13, 30)
}

arousal_data = {ch: [] for ch in channels}  # 存储每个通道的 arousal 数据
timestamps = []  # 存储时间戳

# 开始计算和保存
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    header = ['timestamp'] + [f'{ch}_arousal' for ch in channels]
    writer.writerow(header)

    for start in range(0, len(filtered_data) - window_size + 1, step_size):
        end = start + window_size
        window_data = filtered_data[start:end]
        timestamp = data.iloc[end - 1]['timestamp']  # 使用窗口最后一个样本的时间戳
        row = [timestamp]
        timestamps.append(datetime.fromtimestamp(timestamp))  # 将 Unix 时间戳转换为 datetime 对象
        
        for i, ch_data in enumerate(window_data.T):
            f, psd = welch(ch_data, fs=sfreq, nperseg=512)
            band_psd = {band: np.mean(psd[(f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
            arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
            arousal_data[channels[i]].append(arousal)
            row.append(arousal)
        
        writer.writerow(row)

# 绘制 arousal 数据
plt.figure(figsize=(10, 6))
average_arousal = np.mean([arousal_data[ch] for ch in channels], axis=0)
plt.plot(timestamps, average_arousal, label='Average Arousal', color='lightcoral', linestyle='-')
plt.grid(True)

plt.gca().xaxis.set_major_locator(mdates.HourLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xlabel('Time')
plt.ylabel('Arousal')
plt.title('Arousal over Time for Each Channel and Average')
plt.legend()
plt.tight_layout()
plt.show()
