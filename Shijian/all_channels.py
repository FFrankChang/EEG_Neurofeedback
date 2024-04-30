import numpy as np
import pandas as pd
import csv
import time
from scipy.signal import welch
from queue import Queue

# 假设的频带定义
bands = {'alpha': (8, 12), 'beta': (13, 30), 'theta': (4, 7), 'delta': (1, 3)}
sfreq = 256  # 采样频率

# 读取 CSV 文件并转换成数据队列
df = pd.read_csv("E:\\EEG_Neurofeedback\\data\\20240425_01\\1raw_test.csv")

# 假设有部分数据列不需要用于处理，筛选出来需要的列
eeg_channels = ["Fp1", "Fpz", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FC5", "FC1", 
                "FC2", "FC6", "M1", "T7", "C3", "Cz", "C4", "T8", "M2", "CP5", 
                "CP1", "CP2", "CP6", "P7", "P3", "Pz", "P4", "P8", "POz", "O1", "Oz", "O2"]

data_queue = Queue()

for idx, row in df[eeg_channels].iterrows():
    data_queue.put(row.values)

# 定义其他必要变量
full_names = eeg_channels
num_channels = len(full_names)
processed_data_file = 'processed_data.csv'

# 定义 UDP 通信设定
udp_ip = '127.0.0.1'
udp_port = 12345
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 定义带通滤波器函数
def bandpass_filter(data, fs):
    from scipy.signal import butter, filtfilt
    b, a = butter(3, [0.5/(fs/2), 30/(fs/2)], btype='band')
    return filtfilt(b, a, data)

# 运行 data_processor 函数
def data_processor(selected_channels, window_size=1000, step_size=100):
    channel_indices = [full_names.index(ch) for ch in selected_channels]
    samples = [np.zeros(num_channels) for _ in range(window_size)]
    with open(processed_data_file, 'w', newline='') as file:
        processed_header = ['timestamp', 'alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg', 'arousal']
        writer = csv.writer(file)
        writer.writerow(processed_header)
        count = 0
        try:
            while True:
                if not data_queue.empty():
                    sample = data_queue.get()
                    samples.append(sample)
                    if len(samples) > window_size:
                        samples.pop(0)
                    count += 1
                    if count == step_size:
                        start_time = time.time()
                        selected_samples = np.array(samples[-window_size:])[:, channel_indices]
                        filtered_samples = np.array([bandpass_filter(selected_samples[:, i], fs=sfreq) for i in range(len(selected_channels))])
                        f, psd = welch(filtered_samples, fs=sfreq, nperseg=512)
                        band_psd = {band: np.mean(psd[:, (f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
                        arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
                        result = [time.time()] + [band_psd[band] for band in ['alpha', 'beta', 'theta', 'delta']] + [arousal]
                        writer.writerow(result)
                        file.flush()
                        message = f"arousal:{arousal:.3f}"
                        sock.sendto(message.encode(), (udp_ip, udp_port))
                        print(f"Processing time: {time.time() - start_time:.5f} s")
                        count = 0
        except KeyboardInterrupt:
            print("Received interrupt, closing file.")
            file.close()

# 运行函数
selected_channels = ["Fp1", "Fpz", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FC5", "FC1", "FC2",
                 "FC6", "M1", "T7", "C3", "Cz", "C4", "T8", "M2", "CP5", "CP1", "CP2", 
                 "CP6", "P7", "P3", "Pz", "P4", "P8", "POz", "O1", "Oz", "O2"]  # 可根据需求选择
data_processor(selected_channels)
