from pylsl import StreamInlet, resolve_stream
import time
import threading
from queue import Queue
import numpy as np
import pandas as pd
from scipy.signal import welch, butter, filtfilt

# Resolve stream and create inlet
streams = resolve_stream('name', 'MockStream')
inlet = StreamInlet(streams[0])

data_queue = Queue()

# For saving raw data
raw_data_file = 'raw_eeg_data.csv'
# For saving processed data
processed_data_file = 'alpha_band_psd.csv'

# Band-pass filter setup
def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=1000.0, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def data_receiver():
    last_time = time.time()
    count = 0
    with open(raw_data_file, 'w', newline='') as file:
        while True:
            samples, timestamps = inlet.pull_chunk()
            if timestamps:
                for sample in samples:
                    data_queue.put(sample)
                    count+=1
                    current_time = time.time()
                    # Write raw data to CSV
                    file.write(','.join(map(str, sample)) + '\n')
                    if current_time - last_time >= 1.0:
                        print(f"Samples per second: {count}")
                        count = 0
                        last_time = current_time


def data_processor():
    # Initialize with 1000 zero-filled samples for 3 channels
    samples = [np.zeros(3) for _ in range(1000)]
    while True:
        while not data_queue.empty():
            sample = data_queue.get()
            samples.append(sample)
            if len(samples) > 1000:
                samples.pop(0)
            
            # Process the window of 1000 samples every time the queue length hits a multiple of 100
            if len(samples) == 1000 and len(data_queue.queue) % 100 == 0:
                filtered_samples = np.array([bandpass_filter(np.array(samples)[:, i]) for i in range(3)])
                f, psd = welch(filtered_samples, fs=1000, nperseg=512)
                alpha_idx = np.where((f >= 9) & (f <= 13))
                alpha_psd = np.mean(psd[:, alpha_idx], axis=2)
                
                # Save alpha band PSD to another CSV
                with open(processed_data_file, 'a', newline='') as file:
                    for channel_psd in alpha_psd:
                        file.write(','.join(map(str, channel_psd)) + '\n')

receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, daemon=True)
receiver_thread.start()
processor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Received interrupt, stopping threads.")
