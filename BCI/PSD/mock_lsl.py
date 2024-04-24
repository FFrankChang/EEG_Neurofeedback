import time
from random import uniform
from pylsl import StreamInfo, StreamOutlet

# 用户可以设置的发送频率
frequency = 1000  # 默认频率为1000 Hz, 可以修改为任意值

info = StreamInfo('MockStream', 'EEG', 3, frequency, 'float32', 'myuid34234')
outlet = StreamOutlet(info)

start_time = time.time()
sample_count = 0

try:
    print(f"Sending data at {frequency} Hz...")
    while True:
        # 创建样本数据
        sample = [uniform(200, 300), uniform(200, 300), uniform(-1000, -900)]
        outlet.push_sample(sample)
        sample_count += 1

        # 计算应该发送下一个样本的时间
        next_sample_time = start_time + (sample_count / frequency)
        sleep_time = max(0, next_sample_time - time.time())
        
        # 休眠直到下一个样本发送时间
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    print("Stream stopped.")
