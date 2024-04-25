import pandas as pd
import matplotlib.pyplot as plt
import os

# 数据加载路径
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(base_path, 'data', 'psd_20240425_204556_pre.csv')

# 加载数据并去除前10行
data_cleaned = pd.read_csv(data_path).iloc[10:]

# 计算arousal的平均值和标准差
arousal_mean = data_cleaned['arousal'].mean()
arousal_std = data_cleaned['arousal'].std()

# 计算时间差
time_diff = data_cleaned['timestamp'].iloc[-1] - data_cleaned['timestamp'].iloc[0]

# 创建图表和两个y轴
fig, ax1 = plt.subplots(figsize=(12, 6))

# 设定颜色列表
colors = ['blue', 'green', 'purple', 'orange']

# 绘制alpha_avg, beta_avg, theta_avg, delta_avg在主轴上
for idx, column in enumerate(['alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg']):
    ax1.plot(data_cleaned['timestamp'], data_cleaned[column], label=column, alpha=0.2, color=colors[idx])

# 设置主轴的标签和标题
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Brain Wave Averages')
ax1.set_title('Brain EEG Averages with Arousal Highlighted')
ax1.grid(True)

# 创建第二个y轴用于arousal
ax2 = ax1.twinx()
ax2.plot(data_cleaned['timestamp'], data_cleaned['arousal'], 'lightcoral', label='arousal', linewidth=2)
ax2.set_ylabel('Arousal')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

file_name = os.path.splitext(os.path.basename(data_path))[0]
plt.savefig(os.path.join(os.path.dirname(data_path), f'{file_name}.png'))

print(f"Arousal Mean: {arousal_mean:.4f}")
print(f"Arousal Standard Deviation: {arousal_std:.4f}")
print(f"Duration: {time_diff:.4f} seconds")

# 显示图表
plt.show()
