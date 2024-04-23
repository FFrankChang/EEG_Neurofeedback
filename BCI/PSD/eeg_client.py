import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import xml.etree.ElementTree as ET
import keyboard
import socket
import csv
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
        if channel_type.upper() == 'EEG' and name in ['F7', 'F8', 'P7','P8']:
            channel_names.append(name)
    # channel_names.append('bip')
    return channel_names,full_names

udp_ip = "localhost"
udp_port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
print("Stream found and connected.")

raw_data_file = open('raw_data_final_2.csv', 'w', newline='')
power_bands_file = open('power_bands_final_2.csv', 'w', newline='')
raw_data_writer = csv.writer(raw_data_file)
power_bands_writer = csv.writer(power_bands_file)
channel_names,full_names = get_channel_names_from_info(inlet.info())
raw_data_writer.writerow(['Timestamp_EEG', 'Sample','timestamp_local',full_names])

sfreq = inlet.info().nominal_srate()
sfreq = 1000  # Sampling frequency is 1000 Hz
samples_per_epoch = 1000  # 1 second worth of data at 1000 Hz
step_samples = 100  # Number of samples per step (0.1 seconds at 1000 Hz)
buffer = np.zeros((samples_per_epoch, len(channel_names)))

while True:
    if keyboard.is_pressed('esc'):
        print("Escape key pressed, exiting loop.")
        break

    sample, timestamp = inlet.pull_sample()
    if sample:
        raw_data_writer.writerow([time.time(),sample,timestamp])
        buffer = np.roll(buffer, -step_samples, axis=0)  # Shift data to the left
        buffer[-step_samples:] = sample[4:6]+ sample[22:24] # Insert new samples at the end

        if len(buffer) >= samples_per_epoch:
            data = buffer.T  # Transpose for MNE processing
            ch_types = ['eeg'] * len(channel_names)
            info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=ch_types)
            raw = mne.io.RawArray(data, info)
            raw.filter(1, 40, fir_design='firwin')

            spectrum = raw.compute_psd(method='welch', fmin=1, fmax=40, n_jobs=1)
            freqs = spectrum.freqs
            psd_data = spectrum.get_data()

            bands = {'alpha': (8, 12), 'beta': (13, 30), 'theta': (4, 7), 'delta': (1, 3)}
            power_bands = {band: np.mean(psd_data[:, np.logical_and(freqs >= freq_range[0], freqs <= freq_range[1])], axis=1) for band, freq_range in bands.items()}            
            alpha_mean = np.mean(power_bands['alpha'])
            beta_mean = np.mean(power_bands['beta'])
            theta_mean = np.mean(power_bands['theta'])
            delta_mean = np.mean(power_bands['delta'])
            arousal = (alpha_mean + beta_mean) / (theta_mean + delta_mean)
            power_bands_writer.writerow([time.time(),power_bands,arousal])

            message = f"arousal:{arousal}"
            sock.sendto(message.encode(), (udp_ip, udp_port))
            raw.close()

raw_data_file.close()
power_bands_file.close()