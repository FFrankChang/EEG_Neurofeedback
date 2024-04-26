import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def calculate_heart_rate(ecg_data, sampling_rate):
    # 寻找心电信号的峰值，即R波
    peaks, _ = find_peaks(ecg_data, distance=sampling_rate/2)
    # 计算R-R间隔
    rr_intervals = np.diff(peaks) / sampling_rate * 1000  # 转换为毫秒
    # 计算心率
    heart_rate = 60 / (rr_intervals / 1000)  # 每分钟的心跳数
    return heart_rate,  peaks[1:]

def calculate_hrv(rr_intervals):
    # 计算心率变异性，这里使用SDNN（标准差）
    sdnn = np.std(rr_intervals)
    return sdnn

def plot_heart_rate(heart_rate, heart_rate_times, mode_times, collision_times):
    plt.figure(figsize=(10, 5))
    plt.plot(heart_rate_times, heart_rate, label='Heart Rate')
    # 添加模式切换的竖线
    for event_time in mode_times:
        plt.axvline(x=event_time, color='lightcoral', linestyle='--', label='Mode Switched' if 'Mode Switched' not in plt.gca().get_legend_handles_labels()[1] else "")
    # 添加碰撞事件的竖线
    for collision_time in collision_times:
        plt.axvline(x=collision_time, color='black', linestyle='-.', label='Collision' if 'Collision' not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.xlabel('Time')
    plt.ylabel('Heart Rate (beats per minute)')
    plt.title('Heart Rate Over Time')
    plt.legend()
    plt.show()

# 读取心电数据CSV
ecg_file_path = 'raw_data_0425_02.csv'
sampling_rate = 1000  
ecg_data = pd.read_csv(ecg_file_path)
ecg_values = ecg_data['BIP 01'].values

# 读取模式切换数据CSV
mode_file_path = 'mainvehicle_20240425170754_1_TTC.csv'
mode_data = pd.read_csv(mode_file_path)
mode_times = mode_data[mode_data['Mode_Switched'] == 'Yes']['Time']
collision_times = mode_data[mode_data['Collision'] == 'Yes']['Time']

# 计算心率
heart_rate, peaks = calculate_heart_rate(ecg_values, sampling_rate)
heart_rate_times = ecg_data['timestamp'].iloc[peaks].values  # 心率时间戳

# 计算R-R间隔和HRV
rr_intervals = np.diff(np.where(np.diff(ecg_values) > 0)[0]) / sampling_rate * 1000
hrv = calculate_hrv(rr_intervals)
print("HRV (SDNN):", hrv)

# 绘制心率图并标记模式切换和碰撞时间
plot_heart_rate(heart_rate, heart_rate_times, mode_times, collision_times)
