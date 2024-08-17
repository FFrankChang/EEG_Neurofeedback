import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设置 Arousal 和 Workload 的范围
arousal = np.linspace(0, 1, 100)
workload = np.linspace(0, 1, 100)

# 创建网格
A, W = np.meshgrid(arousal, workload)

# 设置 lambda 参数
lambda_param = 1  # 可以调整这个值以观察不同的效果

# 计算奖励函数
R = -(A - 0.5)**2 - lambda_param * W
# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制表面图
surf = ax.plot_surface(A, W, R, cmap='viridis', edgecolor='none')

# 标签和标题
ax.set_xlabel('Arousal')
ax.set_ylabel('Workload')
ax.set_zlabel('Reward')
ax.set_title('Reward Function Visualization')

# 添加颜色条
fig.colorbar(surf)

plt.show()
