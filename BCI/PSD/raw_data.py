import socket
import json
import csv
import time
from threading import Thread, Event
from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import os
import xml.etree.ElementTree as ET

eye_frame_count = 0
eeg_frame_count = 0

def get_channel_names_from_info(info):
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        channel_names.append(name)
    return channel_names

def udp_data_receiver(output_dir, file_name, stop_event):
    global eye_frame_count
    host = '0.0.0.0'
    port = 1999
    output_file = os.path.join(output_dir, file_name)
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            print(f"Listening on {host}:{port}")
            while not stop_event.is_set():
                data, addr = s.recvfrom(8192)
                try:
                    json_data = json.loads(data.decode())
                    json_data['timestamp'] = time.time()
                    writer.writerow({field: json_data.get(field, '') for field in headers})
                    eye_frame_count += 1
                    if eye_frame_count % 180 == 0:
                        file.flush()
                except json.JSONDecodeError:
                    print("Received non-JSON data")

def lsl_data_receiver(output_dir, file_name, stop_event):
    global eeg_frame_count
    streams = resolve_stream('name', 'SAGA')
    inlet = StreamInlet(streams[0])
    full_names = get_channel_names_from_info(inlet.info())

    output_file = os.path.join(output_dir, file_name)
    with open(output_file, 'w', newline='') as file:
        header = ['timestamp'] + full_names + ['machine_timestamp']
        writer = csv.writer(file)
        writer.writerow(header)
        while not stop_event.is_set():
            samples, timestamps = inlet.pull_chunk()
            if timestamps:
                for sample, timestamp in zip(samples, timestamps):
                    row = [time.time()] + sample + [timestamp]
                    writer.writerow(row)
                    eeg_frame_count += 1
                    if eeg_frame_count % 3000 ==0:
                        file.flush()

def print_frame_rates():
    global eye_frame_count, eeg_frame_count
    while not stop_event.is_set():
        time.sleep(1)
        print(f"EYE {eye_frame_count},EEG {eeg_frame_count}")
        eye_frame_count = 0
        eeg_frame_count = 0

def main():
    global stop_event
    stop_event = Event()
    current_date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    base_path = 'F:\\NFB_EXP\\Exp_V2_data'

    eye_data_filename = f'EYE_{current_date_time}.csv'
    eeg_data_filename = f'EEG_{current_date_time}.csv'

    with open(r'E:\EEG_Neurofeedback\config.txt', 'r') as config_file:
        global headers
        headers = config_file.read().strip().split('\n')

    udp_thread = Thread(target=udp_data_receiver, args=(base_path, eye_data_filename, stop_event))
    lsl_thread = Thread(target=lsl_data_receiver, args=(base_path, eeg_data_filename, stop_event))
    frame_rate_thread = Thread(target=print_frame_rates)

    udp_thread.daemon = True
    lsl_thread.daemon = True
    frame_rate_thread.daemon = True

    udp_thread.start()
    lsl_thread.start()
    frame_rate_thread.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        stop_event.set()

    udp_thread.join()
    lsl_thread.join()
    frame_rate_thread.join()
    print("Threads successfully closed.")

if __name__ == "__main__":
    main()
