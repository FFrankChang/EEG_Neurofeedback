from pylsl import StreamInlet, resolve_stream
import time
import threading
from queue import Queue
import numpy as np
import socket
import xml.etree.ElementTree as ET
import csv
from scipy.signal import welch, butter, filtfilt
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
streams = resolve_stream('name', 'SAGA')
inlet = StreamInlet(streams[0])
full_names = get_channel_names_from_info(inlet.info())
# full_names = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8', 'FC1', 'FC2', 'FC5', 'FC6', 'Cz', 'C3', 'C4', 'T7', 'T8', 'CP1', 'CP2', 'CP5', 'CP6', 'Pz', 'P3', 'P4', 'P7', 'P8', 'PO3', 'PO4', 'Oz', 'O1', 'O2', 'A2', 'A1'] 
num_channels = len(full_names)  
sfreq = inlet.info().nominal_srate()

data_queue = Queue()
current_date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_directory = os.path.join(base_path, 'data')
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# ex_type = 'pre'
ex_type = 'final'
raw_data_file = os.path.join(data_directory, f'eegraw_{current_date_time}_{ex_type}.csv')
processed_data_file = os.path.join(data_directory, f'psd_{current_date_time}_{ex_type}.csv')
udp_ip = "localhost"
udp_port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bands = {
    'delta': (0.5, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (15, 30)
}

def bandpass_filter(data, lowcut=0.5, highcut=40.0, fs=sfreq, order=4):
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
    # Pre-fill the samples array with zeros to avoid delay in initial data processing
    samples = [np.zeros(num_channels) for _ in range(window_size)]
    with open(processed_data_file, 'w', newline='') as file:
        processed_header = ['timestamp', 'alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg', 'arousal']
        writer = csv.writer(file)
        writer.writerow(processed_header)
        count = 0  # This will track the number of samples processed since the last window slide
        try:
            while True:
                if not data_queue.empty():
                    sample = data_queue.get()
                    samples.append(sample)
                    if len(samples) > window_size:
                        samples.pop(0)  # Maintain sliding window size by removing the oldest sample
                    count += 1
                    # Process the samples if the count reaches the step size
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
                        count = 0  # Reset count after processing
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
