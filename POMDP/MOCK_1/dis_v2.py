import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 生成示例数据
np.random.seed(0)
data = np.random.normal(70, 10, 1000)  # 生成平均值为70，标准差为10的正态分布数据

# 计算50%和75%的分位数
median = np.percentile(data, 50)
percentile_75 = np.percentile(data, 75)

# 绘制直方图
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data, bins=30, density=True, alpha=0.6, color='skyblue')

# 绘制正态分布曲线
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, np.mean(data), np.std(data))
plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution')

# 添加50%和75%分位数的垂直线
plt.axvline(median, color='r', linestyle='--', linewidth=2, label='50% (Median)')
plt.axvline(percentile_75, color='r', linestyle='-.', linewidth=2, label='75% Percentile')

# 添加标题和标签
plt.title('Histogram with 50% and 75% Percentiles & Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Density')

# 添加图例
plt.legend()

# 显示图形
plt.show()
