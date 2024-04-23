import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import xml.etree.ElementTree as ET
import keyboard
import threading
import time

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

def process_data(buffer, sfreq, channel_names):
    while True:
        data_ready.wait()  # Wait for signal that new data is ready
        data_ready.clear()

        with buffer_lock:
            data = buffer.copy().T  # Transpose for MNE processing
            print(data)
        # Create MNE RawArray for processing
        # info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=['eeg'] * len(channel_names))
        # raw = mne.io.RawArray(data, info)
        # raw.filter(1, 40, fir_design='firwin')

        # # Compute PSD
        # psd, freqs = mne.time_frequency.psd_welch(raw, fmin=1, fmax=40, n_per_seg=256, n_overlap=128, n_jobs=1)
        # bands = {'alpha': (8, 12), 'beta': (13, 30), 'theta': (4, 7), 'delta': (1, 3)}
        # power_bands = {band: np.mean(psd[:, (freqs >= freq_range[0]) & (freqs <= freq_range[1])], axis=1) for band, freq_range in bands.items()}

        # print(f"Calculated power bands: {power_bands}")

        # raw.close()

print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
print("Stream found and connected.")

channel_names, full_names = get_channel_names_from_info(inlet.info())
sfreq = inlet.info().nominal_srate()
samples_per_epoch = 1000
step_samples = 100
buffer = np.zeros((samples_per_epoch, len(channel_names)))

data_ready = threading.Event()
buffer_lock = threading.Lock()

processing_thread = threading.Thread(target=process_data, args=(buffer, sfreq, channel_names))
processing_thread.start()

try:
    while True:
        if keyboard.is_pressed('esc'):
            print("Escape key pressed, exiting loop.")
            break

        sample, timestamp = inlet.pull_sample()
        print(sample)
        if sample:
            with buffer_lock:
                buffer = np.roll(buffer, -step_samples, axis=0)  # Shift data to the left
                buffer[-step_samples:] = np.array(sample[:3]).reshape(step_samples, -1)  # Insert new samples at the end
                print(buffer)
            if len(buffer) >= samples_per_epoch:
                data_ready.set()  # Signal the processing thread that data is ready
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    processing_thread.join()  # Ensure the processing thread is cleanly stopped
