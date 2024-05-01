import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt
import csv

# 参数设置
file_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\data\\20240430_01_final_02\\eegraw_20240430_152635_final.csv'  # 原始数据文件路径
output_file = 'processed_arousal_values.csv'  # 输出文件路径
sfreq = 1000  
window_size = 1000
step_size = 100
channels = ['F7', 'F8', 'P7', 'P8']  # 实时处理时使用的通道列表

# 读取数据
data = pd.read_csv(file_path)

# 带通滤波函数，修改为可以处理数据的部分片段
def bandpass_filter(data_segment, lowcut=1.0, highcut=40.0, fs=sfreq, order=5):
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
    header = ['timestamp'] + [f'{ch}_arousal' for ch in channels]
    writer.writerow(header)

    # 类似实时处理，应用滑动窗口滤波
    for start in range(0, len(data) - window_size + 1, step_size):
        end = start + window_size
        # 这里选择窗口数据
        window_data = data.loc[start:end-1, channels]
        # 对窗口数据应用滤波
        filtered_data = bandpass_filter(window_data.values)
        timestamp = data.iloc[end - 1]['timestamp']  # 使用窗口最后一个样本的时间戳
        row = [timestamp]
        
        # 计算每个通道的arousal
        for i, ch_data in enumerate(filtered_data.T):
            f, psd = welch(ch_data, fs=sfreq, nperseg=512)
            band_psd = {band: np.mean(psd[(f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
            arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
            row.append(arousal)
        
        writer.writerow(row)
