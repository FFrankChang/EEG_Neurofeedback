from pylsl import StreamInlet, resolve_stream
import numpy as np
import threading
from queue import Queue
import joblib
import csv
from collections import deque
import time
from scipy.signal import welch, butter, filtfilt
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from scipy.linalg import eigh

def get_channel_names_from_info(info):
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        channel_names.append(name)
    return channel_names

def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=1000, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def filter_band(data,band):
    nyq = 0.5 * 1000
    low = band[0] / nyq
    high = band[1] / nyq
    b, a = butter(4, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def calculate_covariance_matrix(data):
    """Calculate the covariance matrix for given EEG data."""
    return np.cov(data, rowvar=False)

def compute_FBCSP(eeg_data_class1, eeg_data_class2, alpha):
    frequency_bands = [(0.5, 4), (4, 8), (8, 15), (15, 24), (24, 50)]
    projection_matrices = []

    for band in frequency_bands:
        # Filter data for each band
        # Assuming filter_band is a function that filters data within a specific frequency band
        filtered_data_class1 = filter_band(eeg_data_class1, band)
        filtered_data_class2 = filter_band(eeg_data_class2, band)

        # Calculate covariance matrices for both classes
        C1 = calculate_covariance_matrix(filtered_data_class1)
        C2 = calculate_covariance_matrix(filtered_data_class2)

        # Calculate the composite covariance matrices using the formula from the paper
        M1 = np.linalg.inv(C1 + alpha * np.eye(C1.shape[0]))
        M2 = np.linalg.inv(C2 + alpha * np.eye(C2.shape[0]))

        # Eigendecomposition
        eigenvalues1, eigenvectors1 = eigh(M1, subset_by_index=[0, 2])
        eigenvalues2, eigenvectors2 = eigh(M2, subset_by_index=[0, 2])

        # Collect eigenvectors corresponding to the largest eigenvalues
        projection_matrices.append(eigenvectors1[:, -3:])
        projection_matrices.append(eigenvectors2[:, -3:])

    # Concatenate all projection matrices
    return np.hstack(projection_matrices)

ex_type = ''
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_directory = os.path.join(base_path, 'data')
current_date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
processed_data_file = os.path.join(data_directory, f'lda_{current_date_time}_{ex_type}.csv')

# 加载LDA模型
lda_model_path = 'lda_game_v2.pkl'  # 模型路径
lda = joblib.load(lda_model_path)
sfreq = 1000
# 解析流并创建输入口
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

data_queue = Queue()
results_queue = deque(maxlen=2000)  

csv_file = open(processed_data_file, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Arousal'])

def data_receiver():
    while True:
        sample, timestamp = inlet.pull_sample()
        data_queue.put((sample, timestamp))

def data_processor():
    sample_count = 0  
    while True:
        if not data_queue.empty():
            sample, timestamp = data_queue.get()
            prediction = lda.predict(np.array([sample]))
            results_queue.append(prediction[0])  

            sample_count += 1
            if sample_count == 200:
                arousal = np.mean(results_queue)
                print(f"Timestamp: {time.time()}, Arousal: {arousal:.3f}")
                csv_writer.writerow([time.time(), arousal])
                csv_file.flush()
                sample_count = 0 

receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, daemon=True)

receiver_thread.start()
processor_thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("程序被中断")
    csv_file.close()
