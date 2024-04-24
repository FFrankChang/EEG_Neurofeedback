from pylsl import StreamInlet, resolve_stream
import time
import threading
from queue import Queue
import numpy as np
import pandas as pd
import socket
import xml.etree.ElementTree as ET
import csv
from scipy.signal import welch, butter, filtfilt
import matplotlib.pyplot as plt

def get_channel_names_from_info(info):
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    EEG_channel_names = []
    full_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        full_names.append(name)
        channel_type = channel.find('type').text
        if channel_type.upper() == 'EEG' and name in ['F7', 'F8', 'P7','P8']:
            EEG_channel_names.append(name)
    return EEG_channel_names,full_names

# Resolve stream and create inlet
streams = resolve_stream('name', 'MockStream')
inlet = StreamInlet(streams[0])
# channel_names, full_names = get_channel_names_from_info(inlet.info())
full_names = ['F7', 'F8', 'P7']
num_channels = 32  # Set this to the number of EEG channels
sfreq = inlet.info().nominal_srate()

data_queue = Queue()
raw_data_file = 'raw_eeg_data.csv'
processed_data_file = 'alpha_band_psd.csv'
udp_ip = "localhost"
udp_port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bands = {
    'delta': (1, 3),
    'theta': (4, 7),
    'alpha': (8, 12),
    'beta': (13, 30)
}
# Band-pass filter setup
def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=1000.0, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def data_receiver():
    with open(raw_data_file, 'w', newline='') as file:
        # header = ['timestamp'] + full_names + ['mechine_timestamp']
        # file.write(','.join(header) + '\n')
        # print(header)
        while True:
            samples, timestamps = inlet.pull_chunk()
            if timestamps:
                for sample, timestamp in zip(samples, timestamps):
                    data_queue.put(sample)
                    # Write raw data with timestamp to CSV
                    data_str = ','.join(map(str,[time.time()]  + sample + [timestamp]))
                    file.write(data_str + '\n')

def data_processor():
    samples = [np.zeros(num_channels) for _ in range(1000)]
    count = 0
    with open(processed_data_file, 'w', newline='') as file:
        processed_header = ['timestamp', 'alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg', 'arousal']
        file.write(','.join(processed_header) + '\n')
        writer = csv.writer(file)
        try:
            while True:
                while not data_queue.empty():
                    sample = data_queue.get()
                    samples.append(sample)
                    if len(samples) > 1000:
                        samples.pop(0)
                    count += 1
                    if count >= 100:
                        start_time = time.time()  # Start time for performance measurement

                        # Convert list of samples to a NumPy array for easier slicing
                        samples_array = np.array(samples)

                        # Plot each channel's data and save to files
                        for i in range(1):
                            plt.figure(figsize=(10, 4))
                            plt.plot(samples_array[:, i], label=f'Channel {i}')  # Now using NumPy array slicing
                            plt.title(f'Channel {i} Data Plot')
                            plt.xlabel('Sample Number')
                            plt.ylabel('Amplitude')
                            plt.legend()
                            plt.savefig(f'channel_{i}_plot_{time.time()}.png')
                            plt.close()

                        filtered_samples = np.array([bandpass_filter(samples_array[:, i]) for i in range(num_channels)])
                        f, psd = welch(filtered_samples, fs=1000, nperseg=512)
                        band_psd = {band: np.mean(psd[:, (f >= low) & (f <= high)]) for band, (low, high) in bands.items()}
                        num = band_psd['alpha'] + band_psd['beta']
                        den = band_psd['theta'] + band_psd['delta']
                        arousal = num / den if den != 0 else float('inf')
                        result = [time.time(), band_psd['alpha'], band_psd['beta'], band_psd['theta'], band_psd['delta'], arousal]
                        writer.writerow(result)
                        file.flush()
                        message = f"arousal:{arousal}"
                        sock.sendto(message.encode(), (udp_ip, udp_port))
                        elapsed_time = time.time() - start_time  # Calculate elapsed time
                        print(f"Processing time for current window: {elapsed_time:.5f} seconds")
                        count = 0
        except KeyboardInterrupt:
            print("Received interrupt, closing file.")
            file.close()

receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, daemon=True)
receiver_thread.start()
processor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Received interrupt, stopping threads.")
