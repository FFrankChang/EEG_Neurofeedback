import time
from random import uniform
from pylsl import StreamInfo, StreamOutlet
import xml.etree.ElementTree as ET

# Define channel names
channel_labels = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8', 'FC1', 'FC2', 'FC5', 'FC6', 'Cz', 'C3', 'C4', 'T7', 'T8', 'CP1', 'CP2', 'CP5', 'CP6', 'Pz', 'P3', 'P4', 'P7', 'P8', 'PO3', 'PO4', 'Oz', 'O1', 'O2', 'A2', 'A1']
channels = len(channel_labels)
frequency = 1000  # Sample frequency in Hz

# Create StreamInfo with channel labels
info = StreamInfo('MockStream', 'EEG', channels, frequency, 'float32', 'myuid34234')

# Adding channel names to the info object
channels_element = info.desc().append_child("channels")
for label in channel_labels:
    ch = channels_element.append_child("channel")
    ch.append_child_value("label", label)
    ch.append_child_value("unit", "microvolts")
    ch.append_child_value("type", "EEG")

outlet = StreamOutlet(info)

start_time = time.time()
sample_count = 0

try:
    print(f"Sending data at {frequency} Hz with {channels} channels...")
    last_time = time.time()
    count = 0
    while True:
        sample = [uniform(0, 1000) for _ in range(channels)]
        outlet.push_sample(sample)
        sample_count += 1
        count += 1
        current_time = time.time()
        if current_time - last_time >= 1.0:
            print(f"Frames per second: {count}")
            count = 0
            last_time = current_time
        next_sample_time = start_time + (sample_count / frequency)
        sleep_time = max(0, next_sample_time - time.time())
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    print("Stream stopped.")
