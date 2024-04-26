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
    return heart_rate

def calculate_hrv(rr_intervals):
    # 计算心率变异性，这里使用SDNN（标准差）
    sdnn = np.std(rr_intervals)
    return sdnn

def plot_heart_rate(heart_rate):
    plt.figure(figsize=(10, 5))
    plt.plot(heart_rate, label='Heart Rate')
    plt.xlabel('Time')
    plt.ylabel('Heart Rate (beats per minute)')
    plt.title('Heart Rate Over Time')
    plt.legend()
    plt.show()

# 读取CSV数据
file_path = 'raw_data_0425_02.csv'
sampling_rate = 1000  
data = pd.read_csv(file_path)
ecg_data = data['BIP 01'].values

# 计算心率
heart_rate = calculate_heart_rate(ecg_data, sampling_rate)
print("Heart Rate:", heart_rate)

# 计算R-R间隔和HRV
rr_intervals = np.diff(np.where(np.diff(ecg_data) > 0)[0]) / sampling_rate * 1000
hrv = calculate_hrv(rr_intervals)
print("HRV (SDNN):", hrv)

# 绘制心率图
plot_heart_rate(heart_rate)
