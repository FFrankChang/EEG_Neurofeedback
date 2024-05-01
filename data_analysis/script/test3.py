import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

def process_and_plot_eeg(file_path):
    # 参数设置
    sfreq = 1000  
    window_size = 1000
    step_size = 100
    channels = ['F7', 'F8', 'P7', 'P8']  # 实时处理时使用的通道列表
    output_file = 'processed_arousal_values.csv'  # 输出文件路径

    # 读取数据
    data = pd.read_csv(file_path)

    # 带通滤波函数
    def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=sfreq, order=4):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        y = filtfilt(b, a, data, axis=0)
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
            timestamps.append(pd.to_datetime(timestamp, unit='s').tz_localize('UTC').tz_convert('Asia/Shanghai').tz_localize(None))
            
            for i, ch_data in enumerate(window_data.T):
                f, psd = welch(ch_data, fs=sfreq, nperseg=512)
                band_psd = {band: np.mean(psd[(f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
                arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
                arousal_data[channels[i]].append(arousal)
                row.append(arousal)
            
            writer.writerow(row)
        
    # 绘图
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['lightcoral', 'blue', 'green', 'purple', 'gold']
    ax.plot(timestamps, arousal_data[channels[0]], label='Arousal', color='lightcoral', linewidth=1)
    ax.set_ylabel('Arousal')
    ax.set_xlabel('Time')
    ax.set_title('Brain EEG Averages with Arousal Highlighted')
    ax.grid(True)

    ax2 = ax.twinx()
    for idx, ch in enumerate(channels):
        ax2.plot(timestamps, arousal_data[ch], label=f'{ch} arousal', alpha=0.2, color=colors[idx+1], linewidth=0.5)
    ax2.set_ylabel('Brain Wave Averages')
    
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.show()

# 调用函数进行处理和绘图
file_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\data\\20240430_01_final_01\\eegraw_20240430_152111_final.csv'
process_and_plot_eeg(file_path)
