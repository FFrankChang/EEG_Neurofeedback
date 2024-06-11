import pandas as pd
import numpy as np
from biosppy.signals import ecg
from scipy.signal import find_peaks
import matplotlib
import matplotlib.pyplot as plt

def calculate_pnn35(nn_intervals):
    differences = np.abs(np.diff(nn_intervals))
    count = np.sum(differences > 35)
    return count / len(nn_intervals) * 100 if nn_intervals.size > 1 else 0

def process_ecg_data(file_path):
    # 读取数据
    data = pd.read_csv(file_path)
    ecg_signal = data['BIP 01'].values

    # 设置采样率
    sampling_rate = 1000  # Hz

    # 使用 biosppy 进行 R 波检测
    out = ecg.ecg(signal=ecg_signal, sampling_rate=sampling_rate, show=False)
    r_peaks = out['rpeaks']

    # 计算 NN 间隔（毫秒）
    nn_intervals = np.diff(r_peaks) / sampling_rate * 1000
    print(nn_intervals)
    # 滑动窗口参数
    window_size = 10 * sampling_rate  # 10秒窗口
    step_size = 1 * sampling_rate     # 1秒滑动步长

    # 计算每个窗口的 pNN35
    pnn35_results = []
    for start in range(0, len(ecg_signal) - window_size + 1, step_size):
        end = start + window_size
        # 窗口中的R波索引
        window_r_peaks = r_peaks[(r_peaks >= start) & (r_peaks < end)]
        if len(window_r_peaks) > 1:
            # 计算窗口中的NN间隔
            window_nn_intervals = np.diff(window_r_peaks) / sampling_rate * 1000
            # 计算 pNN35
            pnn35 = calculate_pnn35(window_nn_intervals)
            pnn35_results.append(pnn35)
        else:
            pnn35_results.append(0)

    return pnn35_results

# 调用函数处理数据
file_path = r'D:\gitee\EEG_Neurofeedback\data\20240523_s03_11_hard_feedback\eegraw_20240523_202718_final.csv'
pnn35_values = process_ecg_data(file_path)
plt.plot(pnn35_values)
plt.show()
print(pnn35_values)

