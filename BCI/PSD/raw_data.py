import socket
import json
import csv
import time
import keyboard
from threading import Thread
from pylsl import StreamInlet, resolve_stream
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

def udp_data_receiver(output_dir, file_name):
    host = '0.0.0.0'
    port = 1999
    output_file = os.path.join(output_dir, file_name)
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            print(f"Listening on {host}:{port}")
            while not keyboard.is_pressed('esc'):
                data, addr = s.recvfrom(8192)
                try:
                    json_data = json.loads(data.decode())
                    json_data['timestamp'] = time.time()
                    writer.writerow({field: json_data.get(field, '') for field in headers})
                except json.JSONDecodeError:
                    print("Received non-JSON data")
                except KeyboardInterrupt:
                    print("Program terminated with keyboard interrupt.")
                    break

def lsl_data_receiver(output_dir, file_name):
    streams = resolve_stream('name', 'MockStream')
    inlet = StreamInlet(streams[0])
    full_names = get_channel_names_from_info(inlet.info())

    output_file = os.path.join(output_dir, file_name)
    with open(output_file, 'w', newline='') as file:
        header = ['timestamp'] + full_names + ['machine_timestamp']
        writer = csv.writer(file)
        writer.writerow(header)
        try:
            while True:
                samples, timestamps = inlet.pull_chunk()
                if timestamps:
                    for sample, timestamp in zip(samples, timestamps):
                        row = [time.time()] + sample + [timestamp]
                        writer.writerow(row)
        except KeyboardInterrupt:
            print("LSL data reception interrupted, stopping.")

def main():
    current_date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    base_path = 'F:\\NFB_EXP\\Exp_V2_data\\S01_D01'

    eye_data_filename = f'EYE_{current_date_time}.csv'
    eeg_data_filename = f'EEG_{current_date_time}.csv'

    # Load column headers for UDP data receiver
    with open(r'E:\EEG_Neurofeedback\config.txt', 'r') as config_file:
        global headers
        headers = config_file.read().strip().split('\n')

    # Create threads for each data receiver
    udp_thread = Thread(target=udp_data_receiver, args=(base_path, eye_data_filename))
    lsl_thread = Thread(target=lsl_data_receiver, args=(base_path, eeg_data_filename))

    # Start threads
    udp_thread.start()
    lsl_thread.start()

    # Wait for threads to complete
    udp_thread.join()
    lsl_thread.join()
    print("Data reception completed.")

if __name__ == "__main__":
    main()
