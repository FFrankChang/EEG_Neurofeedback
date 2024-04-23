import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import threading
from queue import Queue
import time  # 导入time模块

# 设置LSL stream
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
channel_names = ['F7', 'F8', 'P7']
sfreq = inlet.info().nominal_srate()
samples_per_epoch = 1000  
step_samples = 100  
buffer = np.zeros((samples_per_epoch, len(channel_names)))

data_queue = Queue()

def data_receiver():
    while True:
        sample, timestamp = inlet.pull_sample()
        if sample:
            data_queue.put(sample[:3])  # 只取前三个通道的数据

def data_processor():
    while True:
        if not data_queue.empty():
            start_time = time.time()  # 开始时间
            for _ in range(step_samples):
                sample = data_queue.get()
                buffer[:-step_samples] = buffer[step_samples:]
                buffer[-step_samples:] = np.array(sample).reshape(-1, len(channel_names))

            # 数据处理
            data = buffer.T
            ch_types = ['eeg'] * len(channel_names)
            info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=ch_types)
            raw = mne.io.RawArray(data, info)
            raw.filter(1, 40, fir_design='firwin')

            spectrum = raw.compute_psd(method='welch', fmin=1, fmax=40, n_jobs=1)
            end_time = time.time()  # 结束时间
            processing_time = end_time - start_time  # 计算处理时间
            print(f"Processing Time: {processing_time} seconds")

            raw.close()

receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, daemon=True)

receiver_thread.start()
processor_thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Received interrupt, stopping threads.")
