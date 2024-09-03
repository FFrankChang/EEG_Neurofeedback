import numpy as np
import matplotlib.pyplot as plt

# 设置正态分布的参数
mean = 0.5  # 均值
std_dev = 0.1  # 标准差
num_samples = 1000  # 样本数量

# 生成正态分布数据
data = np.random.normal(mean, std_dev, num_samples)

# 只保留在 0 到 1 之间的数据
data = data[(data >= 0) & (data <= 1)]

# 绘制正态分布的直方图
plt.figure(figsize=(8, 6))
plt.hist(data, bins=30, density=True, alpha=0.6, color='g')

# 生成x轴数据
xmin, xmax = plt.xlim()
x = np.linspace(0, 1, 100)

# 计算正态分布的概率密度函数 (PDF)
p = np.exp(-0.5 * ((x - mean) / std_dev) ** 2) / (std_dev * np.sqrt(2 * np.pi))

# 绘制正态分布曲线
plt.plot(x, p, 'k', linewidth=2)

# 设置标题和标签
plt.title('Normal Distribution (0 to 1)')
plt.xlabel('Value')
plt.ylabel('Probability Density')

# 显示图形
plt.show()
