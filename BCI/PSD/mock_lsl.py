import time
from random import uniform
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo('MockStream', 'EEG', 3, 1000, 'float32', 'myuid34234')
outlet = StreamOutlet(info)
try:
    print("Sending data...")
    while True:
        sample = [uniform(200, 300), uniform(200, 300), uniform(-1000, -900)]
        outlet.push_sample(sample)
        time.sleep(0.001)  
except KeyboardInterrupt:
    print("Stream stopped.")
