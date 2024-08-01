import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Times New Roman'

# 模拟的 p 值数据
p_values = np.array([0.04, 0.2, 0.03, 0.07, 0.01, 0.15])

# 设置柱状图的标签
labels = ['10s', '20s', '30s', '40s', '50s', '60s']

# 创建柱状图
fig, ax = plt.subplots(figsize=(8, 6))
bar_width = 0.6  
index = np.arange(len(labels)) 

# 根据 p 值大小设置柱状图的颜色
colors = ['royalblue' if p < 0.05 else 'grey' for p in p_values]
bars = ax.bar(index, p_values, bar_width, color=colors)

ax.axhline(y=0.05, color='black', linestyle='--', label='Significance level (p=0.05)')

# 设置轴标签
ax.set_ylabel('P Values', fontsize=14)

# 设置刻度标签大小
ax.set_xticks(index)
ax.set_xticklabels(labels, fontsize=12)  # X轴刻度标签大小
ax.tick_params(axis='y', labelsize=12)   # Y轴刻度标签大小

# 设置图例字体大小
ax.legend(fontsize=12)
plt.show()
