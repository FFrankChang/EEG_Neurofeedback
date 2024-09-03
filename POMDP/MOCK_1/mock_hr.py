import matplotlib.pyplot as plt
import numpy as np

# 生成模拟心率数据
heart_rate_data = np.random.normal(loc=70, scale=10, size=1000)

# 计算50%和75%位置的数值
median = np.percentile(heart_rate_data, 50)
percentile_75 = np.percentile(heart_rate_data, 75)

# 绘制心率数据的直方图
plt.figure(figsize=(10, 6))
plt.hist(heart_rate_data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(median, color='lightcoral', linestyle='--', linewidth=2, label='50% (Median)')
plt.axvline(percentile_75, color='lightcoral', linestyle='--', linewidth=2, label='75% Percentile')
plt.title('Heart Rate Histogram with 50% and 75% Percentiles')
plt.xlabel('Heart Rate (beats per minute)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
