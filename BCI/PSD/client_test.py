import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import xml.etree.ElementTree as ET
import threading
import keyboard
import time
import matplotlib.pyplot as plt  # Import matplotlib for plotting

def get_channel_names_from_info(info):
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    full_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        full_names.append(name)
        channel_type = channel.find('type').text
        if channel_type.upper() == 'EEG' and name in ['F7', 'F8', 'P7']:
            channel_names.append(name)
    return channel_names, full_names

def plot_data(data, file_name):
    """Function to plot and save the current buffer data"""
    plt.figure(figsize=(10, 6))
    for i, channel_data in enumerate(data.T):
        plt.subplot(len(data.T), 1, i + 1)
        plt.plot(channel_data)
        plt.title(f"Channel {i + 1}")
        plt.tight_layout()
    plt.savefig(file_name)
    plt.close()

def process_data(buffer, sfreq, channel_names):
    """处理数据，计算PSD，并更新全局buffer"""
    while True:
        data_ready.wait()
        data_ready.clear()
        with data_lock:
            print(buffer)
            # data = buffer.copy()  # 复制数据以进行处理
            # print(data)


# Initialize LSL Stream
print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
print("Stream found and connected.")

channel_names, full_names = get_channel_names_from_info(inlet.info())
sfreq = inlet.info().nominal_srate()
print(sfreq)
samples_per_epoch = 1000
buffer = np.zeros((samples_per_epoch, len(channel_names)))
sample_count = 0  # Track number of samples received

# Thread synchronization tools
data_ready = threading.Event()
data_lock = threading.Lock()

# Start processing thread
processing_thread = threading.Thread(target=process_data, args=(buffer, sfreq, channel_names))
processing_thread.start()

try:
    while True:
        if keyboard.is_pressed('esc'):
            print("Escape key pressed, exiting loop.")
            break

        sample, timestamp = inlet.pull_sample()
        if sample:
            # print(sample)
            with data_lock:
                buffer = np.roll(buffer, -1, axis=0)
                buffer[-1, :] = np.array(sample[:3])  # Update buffer with new data
                # print("Buffer updated:", buffer[-10:, :])
                sample_count += 1  # Increment sample count

                if sample_count >= 1000:
                    sample_count = 0  # Reset sample count after processing
                    data_ready.set()

finally:
    # Ensure the processing thread can terminate
    data_ready.set()  # Ensure that the wait in the thread can complete
    processing_thread.join()
