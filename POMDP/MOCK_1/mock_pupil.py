import matplotlib.pyplot as plt
import numpy as np

# 生成模拟瞳孔大小数据
# 假设瞳孔大小分布为正态分布，平均瞳孔大小为3.5毫米，标准差为0.5毫米
pupil_size_data = np.random.normal(loc=3.5, scale=0.4, size=1000)
pupil_size_data = pupil_size_data[pupil_size_data >= 2.8]

# 计算50%和75%位置的数值
median = np.percentile(pupil_size_data, 50)
percentile_75 = np.percentile(pupil_size_data, 75)

# 绘制瞳孔大小数据的直方图
plt.figure(figsize=(10, 6))
plt.hist(pupil_size_data, bins=30, color='lightblue', edgecolor='black', alpha=0.7)
plt.axvline(median, color='lightcoral', linestyle='--', linewidth=2, label='50% (Median)')
plt.axvline(percentile_75, color='lightcoral', linestyle='--', linewidth=2, label='75% Percentile')
plt.title('Pupil Size Histogram with 50% and 75% Percentiles')
plt.xlabel('Pupil Size (mm)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
