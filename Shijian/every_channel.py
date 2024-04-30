import numpy as np
import pandas as pd
import csv
import time
from scipy.signal import welch, butter, filtfilt
from queue import Queue

# 假设的频带定义
bands = {'alpha': (8, 12), 'beta': (12, 30), 'theta': (4, 8), 'delta': (0.5, 4)}
sfreq = 256  # 采样频率

# 读取 CSV 文件并转换成数据队列
df = pd.read_csv("E:\\EEG_Neurofeedback\\data\\20240425_01\\1raw_test.csv")
eeg_channels = ["Fp1", "Fpz", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FC5", "FC1", "FC2", "FC6",
                "T7", "C3", "Cz", "C4", "T8", "CP5", "CP1", "CP2", "CP6", 
                "P7", "P3", "Pz", "P4", "P8", "POz", "O1", "Oz", "O2"]

data_queue = Queue()
for idx, row in df[eeg_channels].iterrows():
    data_queue.put(row.values)

full_names = eeg_channels
num_channels = len(full_names)
processed_data_file = 'processed_data_every_channel.csv'

def bandpass_filter(data, fs):
    b, a = butter(3, [0.5/(fs/2), 30/(fs/2)], btype='band')
    return filtfilt(b, a, data)

def data_processor(selected_channels, window_size=1000, step_size=100):
    channel_indices = [full_names.index(ch) for ch in selected_channels]
    samples = [np.zeros(num_channels) for _ in range(window_size)]
    with open(processed_data_file, 'w', newline='') as file:
        header = ['timestamp'] + selected_channels  # 修改标题行，为每个通道添加自己的列
        writer = csv.writer(file)
        writer.writerow(header)
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
                        row = [time.time()]
                        for i in range(len(selected_channels)):
                            filtered_sample = bandpass_filter(selected_samples[:, i], fs=sfreq)
                            f, psd = welch(filtered_sample, fs=sfreq, nperseg=512)
                            band_psd = {band: np.mean(psd[(f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
                            arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
                            row.append(arousal)
                        writer.writerow(row)
                        file.flush()
                        print(f"Processing time: {time.time() - start_time:.5f} s")
                        count = 0
        except KeyboardInterrupt:
            print("Received interrupt, closing file.")
            file.close()

selected_channels = eeg_channels  # 修改这里，选择所有通道
data_processor(selected_channels)
