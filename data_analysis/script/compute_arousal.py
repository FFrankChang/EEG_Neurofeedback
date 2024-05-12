import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt
import csv

# 参数设置
file_path = 'D:\Frank_Project\EEG_Neurofeedback\data\eegraw_20240512_163902_final.csv'  # 原始数据文件路径
output_file = 'test.csv'  # 输出文件路径
sfreq = 1000  
window_size = 1000
step_size = 100
channels = ['F7', 'F8', 'P7', 'P8']  # 实时处理时使用的通道列表

# 读取数据
data = pd.read_csv(file_path)

# 带通滤波函数，修改为可以处理数据的部分片段
def bandpass_filter(data_segment, lowcut=1.0, highcut=40.0, fs=sfreq, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data_segment, axis=0)
    return y

# 设置频段
bands = {
    'delta': (1, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (13, 30)
}

# 开始计算和保存
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    header = ['timestamp'] + [f'{ch}_arousal' for ch in channels] + ['mean_arousal']
    writer.writerow(header)  # 写入头部信息

    # 类似实时处理，应用滑动窗口滤波
    for start in range(0, len(data) - window_size + 1, step_size):
        end = start + window_size
        # 这里选择窗口数据
        window_data = data.loc[start:end-1, channels]
        # 对窗口数据应用滤波
        filtered_data = bandpass_filter(window_data.values)
        timestamp = data.iloc[end - 1]['timestamp']  # 使用窗口最后一个样本的时间戳
        row = [timestamp]
        arousal_values = []  # 存储当前窗口的所有 arousal 值
        # 计算每个通道的 arousal
        for i, ch_data in enumerate(filtered_data.T):
            f, psd = welch(ch_data, fs=sfreq, nperseg=500, window='hamming')
            band_psd = {band: np.mean(psd[(f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
            arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
            row.append(arousal)
            arousal_values.append(arousal)

        mean_arousal = np.mean(arousal_values)  # 计算 mean_arousal
        row.append(mean_arousal)  
        writer.writerow(row)  