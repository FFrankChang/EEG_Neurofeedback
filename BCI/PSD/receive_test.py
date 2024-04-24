from pylsl import StreamInlet, resolve_stream
import time
import threading
from queue import Queue
import numpy as np

streams = resolve_stream('name', 'MockStream')
inlet = StreamInlet(streams[0])

data_queue = Queue()

def data_receiver():
    last_time = time.time()
    count = 0
    while True:
        samples, timestamp = inlet.pull_chunk()
        if timestamp:
            for sample in samples:
                data_queue.put(sample)
                count += 1
                current_time = time.time()
                if current_time - last_time >= 1.0:
                    print(f"Samples per second: {count}")
                    count = 0
                    last_time = current_time

def data_processor():
    samples = []
    while True:
        if not data_queue.empty():
            sample = data_queue.get()
            samples.append(sample)
            if len(samples) == 100:
                sample_averages = [np.mean(s) for s in samples]
                overall_average = np.mean(sample_averages)
                print(f"Average of 100 samples: {overall_average}")
                samples = []

receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, daemon=True)
receiver_thread.start()
processor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Received interrupt, stopping threads.")
