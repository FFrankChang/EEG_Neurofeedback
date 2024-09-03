import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 设置采样率
sampling_rate = 10  # Hz，每秒采样10次
duration = 59  # 时间持续到第59秒

# 计算总的样本数
total_samples = sampling_rate * (duration + 1)

# 生成时间戳，每0.1秒一个数据点
timestamps = np.linspace(0, duration, num=total_samples)

# 生成随机数据，0或1
data = np.random.randint(0, 2, total_samples)

# 创建DataFrame来存储数据
df = pd.DataFrame({
    'Timestamp': timestamps,
    'Data': data
})

plt.figure(figsize=(10, 5))
plt.plot(df['Timestamp'], df['Data'], marker='o', linestyle='-', color='lightblue',alpha =0.5)
plt.title('silence test')
plt.xlabel('Time (seconds)')
plt.ylabel('Action')
plt.yticks([0, 1])  # 显示y轴的标签为0和1
plt.grid(True)

# 显示图表
plt.show()
