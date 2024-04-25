import time
from random import uniform
from pylsl import StreamInfo, StreamOutlet

channels = 32

frequency = 1000  

info = StreamInfo('MockStream', 'EEG', channels, frequency, 'float32', 'myuid34234')
outlet = StreamOutlet(info)

start_time = time.time()
sample_count = 0

try:
    print(f"Sending data at {frequency} Hz with {channels} channels...")
    last_time = time.time()
    count  = 0
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
