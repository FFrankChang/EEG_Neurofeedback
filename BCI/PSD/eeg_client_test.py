from pylsl import StreamInlet, resolve_stream
import time
import threading
from queue import Queue
import numpy as np
import csv
from scipy.signal import welch, butter, filtfilt
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def get_channel_names_from_info(info):
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        channel_names.append(name)
    return channel_names

# Resolve stream and create inlet
streams = resolve_stream('name', 'MockStream')
inlet = StreamInlet(streams[0])
# full_names = get_channel_names_from_info(inlet.info())
full_names = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8', 'FC1', 'FC2', 'FC5', 'FC6', 'Cz', 'C3', 'C4', 'T7', 'T8', 'CP1', 'CP2', 'CP5', 'CP6', 'Pz', 'P3', 'P4', 'P7', 'P8', 'PO3', 'PO4', 'Oz', 'O1', 'O2', 'A2', 'A1'] 
num_channels = len(full_names)  
sfreq = inlet.info().nominal_srate()

data_queue = Queue()
current_date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

base_path = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(base_path, 'data')
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

ex_type = 'final'
raw_data_file = os.path.join(data_directory, f'eegraw_{current_date_time}_{ex_type}.csv')
processed_data_file = os.path.join(data_directory, f'arousal_{current_date_time}_{ex_type}.csv')
bands = {
    'delta': (1, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (15, 30)
}

def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=sfreq, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def data_receiver():
    with open(raw_data_file, 'w', newline='') as file:
        header = ['timestamp'] + full_names + ['machine_timestamp']
        writer = csv.writer(file)
        writer.writerow(header)
        while True:
            samples, timestamps = inlet.pull_chunk()
            if timestamps:
                for sample, timestamp in zip(samples, timestamps):
                    data_queue.put(sample)
                    row = [time.time()] + sample + [timestamp]
                    writer.writerow(row)

def data_processor(selected_channels, window_size=1000, step_size=100):
    channel_indices = [full_names.index(ch) for ch in selected_channels]
    samples = [np.zeros(num_channels) for _ in range(window_size)]
    with open(processed_data_file, 'w', newline='') as file:
        processed_header = ['timestamp'] + [f'arousal_{ch}' for ch in selected_channels] + ['arousal_avg']
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
                        selected_samples = np.array(samples[-window_size:])[:, channel_indices]
                        channel_arousals = []
                        for i in range(len(selected_channels)):
                            filtered_sample = bandpass_filter(selected_samples[:, i], fs=sfreq)
                            f, psd = welch(filtered_sample, fs=sfreq, nperseg=500, window='hamming')
                            band_psd = {band: np.mean(psd[(f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
                            arousal = (band_psd['alpha'] + band_psd['beta']) / (band_psd['theta'] + band_psd['delta'])
                            channel_arousals.append(arousal)
                        arousal_avg = np.mean(channel_arousals)
                        result = [time.time()] + channel_arousals + [arousal_avg]
                        writer.writerow(result)
                        file.flush()
                        count = 0
        except KeyboardInterrupt:
            print("Received interrupt, closing file.")
            file.close()

receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, args=(['F7', 'F8', 'P7', 'P8'],), daemon=True)
receiver_thread.start()
processor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Received interrupt, stopping threads.")
