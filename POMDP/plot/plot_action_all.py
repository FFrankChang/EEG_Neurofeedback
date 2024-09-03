import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os  # 导入os模块用于文件路径操作

# 指定文件夹路径
folder_path = r'E:\NFB_data_backup\20240821\csv'

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # 构建完整文件路径
        file_path = os.path.join(folder_path, filename)
        
        # 读取CSV文件
        data = pd.read_csv(file_path)

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
            plt.axvline(x=tor_time, color='lightcoral', linestyle='--', label='Tor Event', alpha=0.8)

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

        # 保存图表为PNG文件，文件名与CSV相同，但扩展名为.png
        plt.savefig(os.path.join(folder_path, filename[:-4] + '.png'))
        plt.close()  # 关闭图形，避免图像重叠
