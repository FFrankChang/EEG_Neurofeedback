import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv('output.csv')

# 将'Timestamp'列转换为datetime类型
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y-%m-%d %H:%M:%S,%f', errors='coerce')

# 初始化一个新列'Signal'，默认值为0
data['Signal'] = 0

# 标记play事件及其后5秒内的数据为1
signal_duration = pd.Timedelta(seconds=5)
play_data = data[data['Info Content'].str.contains('play', case=False, na=False)]
for play_time in play_data['Timestamp']:
    data.loc[(data['Timestamp'] >= play_time) & (data['Timestamp'] <= play_time + signal_duration), 'Signal'] = 1

# 绘制基本的折线图
plt.figure(figsize=(14, 6))
plt.plot(data['Timestamp'], data['Signal'], label='Signal (0 or 1)', color='lightblue')

# 处理并标记所有包含'tor'的事件
tor_data = data[data['Info Content'].str.contains('tor', case=False, na=False)]
for tor_time in tor_data['Timestamp']:
    plt.axvline(x=tor_time, color='lightcoral', linestyle='--', label='Tor Event',alpha =0.8)

# 添加图例
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # 移除重复的图例项
plt.legend(by_label.values(), by_label.keys())

# 标题和轴标签
plt.title('Action Plot')
plt.xlabel('Timestamp')
plt.ylabel('action (0 or 1)')
plt.xticks(rotation=45)
plt.tight_layout()

# 显示图表
plt.show()
