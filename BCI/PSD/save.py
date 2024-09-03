from pylsl import StreamInlet, resolve_stream
import time
import csv
from datetime import datetime
import os
import xml.etree.ElementTree as ET

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
full_names = get_channel_names_from_info(inlet.info())

current_date_time = datetime.now().strftime('%Y%m%d%H%M%S')
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_directory = os.path.join(base_path, 'data')

if not os.path.exists(data_directory):
    os.makedirs(data_directory)

raw_data_file = os.path.join(data_directory, f'eegraw_{current_date_time}.csv')

def data_receiver():
    with open(raw_data_file, 'w', newline='') as file:
        header = ['timestamp'] + full_names + ['machine_timestamp']
        writer = csv.writer(file)
        writer.writerow(header)
        while True:
            samples, timestamps = inlet.pull_chunk()
            if timestamps:
                for sample, timestamp in zip(samples, timestamps):
                    row = [time.time()] + sample + [timestamp]
                    writer.writerow(row)

try:
    data_receiver()
except KeyboardInterrupt:
    print("Received interrupt, stopping data reception.")
