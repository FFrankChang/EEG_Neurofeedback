import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt
import csv

# 参数设置
file_path = r'E:\Faller_et_al_2019_PNAS_EEG_Neurofeedback_VR_Flight\S05_F_CL_Sil_50_100_merged.csv'  # 原始数据文件路径
output_file = 'test2.csv'  # 输出文件路径
sfreq = 256  
window_size = 256
step_size = 25
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
    header = ['time'] + [f'{ch}_{band}' for ch in channels for band in bands.keys()] + ['arousal_pl']
    writer.writerow(header)  # 写入头部信息

    # 类似实时处理，应用滑动窗口滤波
    for start in range(0, len(data) - window_size + 1, step_size):
        end = start + window_size
        # 这里选择窗口数据
        window_data = data.loc[start:end-1, channels]
        # 对窗口数据应用滤波
        filtered_data = bandpass_filter(window_data.values)
        timestamp = data.iloc[end - 1]['time']  # 使用窗口最后一个样本的时间戳
        row = [timestamp]

        # 计算和存储每个通道的频段PSD值
        channel_psd_sums = {band: [] for band in bands}
        for ch_data in filtered_data.T:
            f, psd = welch(ch_data, fs=sfreq, nperseg=256, window='hamming')
            for band, (low, high) in bands.items():
                band_psd = np.mean(psd[(f >= low) & (f <= high)])
                channel_psd_sums[band].append(band_psd)
                row.append(band_psd)

        # 计算四个通道平均值的arousal_pl
        arousal_pl = (np.mean(channel_psd_sums['alpha']) + np.mean(channel_psd_sums['beta'])) / \
                     (np.mean(channel_psd_sums['theta']) + np.mean(channel_psd_sums['delta']))
        row.append(arousal_pl)
        
        writer.writerow(row)  # 写入数据到文件
