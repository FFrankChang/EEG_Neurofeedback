import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# 生成模拟瞳孔大小数据
# 假设瞳孔大小分布为正态分布，平均瞳孔大小为3.5毫米，标准差为0.4毫米
pupil_size_data = np.random.normal(loc=3.5, scale=0.4, size=1000)
pupil_size_data = pupil_size_data[pupil_size_data >= 2.8]  # 过滤掉小于2.8的数据

# 计算50%和75%位置的数值
median = np.percentile(pupil_size_data, 50)
percentile_75 = np.percentile(pupil_size_data, 75)

# 绘制直方图
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(pupil_size_data, bins=30, density=True, alpha=0.6, color='skyblue')

# 计算并绘制正态分布曲线
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, np.mean(pupil_size_data), np.std(pupil_size_data))
plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution')

# 添加50%和75%位置的垂直线
plt.axvline(median, color='r', linestyle='--', linewidth=2, label='50% (Median)')
plt.axvline(percentile_75, color='r', linestyle='-.', linewidth=2, label='75% Percentile')

# 添加标题和标签
plt.title('Pupil Size Distribution with 50% and 75% Percentiles')
plt.xlabel('Pupil Size (mm)')
plt.ylabel('Density')

# 添加图例
plt.legend()

# 显示图形
plt.show()
