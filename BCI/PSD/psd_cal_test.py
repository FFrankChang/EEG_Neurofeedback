import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import xml.etree.ElementTree as ET
import keyboard
import socket

def get_channel_names_from_info(info):
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        channel_type = channel.find('type').text
        if channel_type.upper() == 'EEG' and name in ['AF7', 'AF8', 'TP9', 'TP10']:
            channel_names.append(name)
    return channel_names

# Set up UDP socket
udp_ip = "localhost"
udp_port = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
print("Stream found and connected.")

channel_names = get_channel_names_from_info(inlet.info())
sfreq = inlet.info().nominal_srate()
new_sfreq = 100  # New sampling frequency after resampling
epoch_duration = 0.1  # seconds
overlap = 0.9  # 90% overlap
step_samples = int(new_sfreq * epoch_duration * (1 - overlap))
samples_per_epoch = int(new_sfreq * epoch_duration)
buffer = []

while True:
    if keyboard.is_pressed('esc'):
        print("Escape key pressed, exiting loop.")
        break

    sample, timestamp = inlet.pull_sample()
    if sample:
        buffer.append(sample)

        if len(buffer) >= samples_per_epoch:
            data = np.array(buffer[:samples_per_epoch]).T  # Process the first epoch worth of data
            ch_types = ['eeg'] * len(channel_names)
            info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=ch_types)

            raw = mne.io.RawArray(data, info)
            raw, _ = raw.set_eeg_reference('average', projection=True)
            raw.resample(new_sfreq, npad="auto")
            raw.filter(1, 40, fir_design='firwin')

            spectrum = raw.compute_psd(method='welch', fmin=1, fmax=40, n_jobs=1)
            freqs = spectrum.freqs
            psd_data = spectrum.get_data()

            bands = {'alpha': (8, 12), 'beta': (13, 30), 'theta': (4, 7), 'delta': (1, 3)}
            power_bands = {band: np.mean(psd_data[:, np.logical_and(freqs >= freq_range[0], freqs <= freq_range[1])], axis=1) for band, freq_range in bands.items()}

            # Send power band data through UDP
            message = f"{timestamp},{power_bands['alpha']},{power_bands['beta']},{power_bands['theta']},{power_bands['delta']}"
            sock.sendto(message.encode(), (udp_ip, udp_port))

            # Manage the buffer for overlap
            buffer = buffer[step_samples:]  # Remove processed samples and keep the rest for overlap
