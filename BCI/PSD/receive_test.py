from pylsl import StreamInlet, resolve_stream
import time
import threading
from queue import Queue
import numpy as np

# 解析数据流
streams = resolve_stream('name', 'MockStream')
inlet = StreamInlet(streams[0])

# 创建队列用于线程间通信
data_queue = Queue()

def data_receiver():
    while True:
        # 拉取数据样本
        sample, timestamp = inlet.pull_sample()
        if timestamp:
            # 将数据样本放入队列中
            data_queue.put(sample)

def data_processor():
    samples = []
    while True:
        if not data_queue.empty():
            # 从队列中获取数据
            sample = data_queue.get()
            samples.append(sample)
            # 每100个样本计算一次平均值
            if len(samples) == 100:
                # 计算每个样本的平均值
                sample_averages = [np.mean(s) for s in samples]
                # 计算100个样本的总平均值
                overall_average = np.mean(sample_averages)
                print(f"Average of 100 samples: {overall_average}")
                samples = []

# 创建线程
receiver_thread = threading.Thread(target=data_receiver, daemon=True)
processor_thread = threading.Thread(target=data_processor, daemon=True)

# 启动线程
receiver_thread.start()
processor_thread.start()

# 主线程等待用户中断，例如按下ESC键
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Received interrupt, stopping threads.")
