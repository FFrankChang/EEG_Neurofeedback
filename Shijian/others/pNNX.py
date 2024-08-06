import pandas as pd
import numpy as np
import biosppy
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = r'E:\EEG_Neurofeedback\data\20240523_06_hard(silence)\eegraw_20240523_120238_final.csv'
data = pd.read_csv(file_path)

# 提取心电图数据
ecg_data = data['BIP 01'].values

# 使用biosppy进行R波检测
r_peaks = biosppy.signals.ecg.ecg(signal=ecg_data, sampling_rate=1000.0, show=False)['rpeaks']

# 计算R-R间隔（以毫秒为单位）
rr_intervals = np.diff(r_peaks) * (1000 / 1000.0)

# 定义计算pNN的函数
def calculate_pNN(rr_intervals, threshold_ms):
    rr_differences = np.abs(np.diff(rr_intervals))
    pNN = np.sum(rr_differences > threshold_ms) / len(rr_differences) * 100
    return pNN

# 计算各个pNN指标
thresholds = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
pNN_results = {f'pNN{threshold}ms': calculate_pNN(rr_intervals, threshold) for threshold in thresholds}

# 输出结果
for key, value in pNN_results.items():
    print(f'{key}: {value:.2f}%')

# 可选：绘制R波检测结果
plt.figure(figsize=(10, 4))
plt.plot(ecg_data, label='ECG Signal')
plt.scatter(r_peaks, ecg_data[r_peaks], color='red', label='R Peaks')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.title('R Peaks Detection')
plt.legend()
plt.show()
