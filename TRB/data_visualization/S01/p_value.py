import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Times New Roman'

# 模拟的 p 值数据
p_values_1 = np.array([0.03125, 0.15625, 0.21875, 0.68, 0.21875, 0.21875])
p_values_2 = np.array([0.31, 0.15625, 0.03125, 0.56, 0.84, 0.84])
p_values_3 = np.array([0.43, 0.15625, 0.09375, 0.09375, 0.21875, 0.21875])

# 设置柱状图的标签
labels = ['10s', '20s', '30s', '40s', '50s', '60s']

# 创建三个子图
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 5),sharey=True)  # 调整总图大小
bar_width = 0.8  
index = np.arange(len(labels)) 

def plot_ax(ax, p_values, title,y_lable = None):
    colors = ['royalblue' if p < 0.05 else 'grey' for p in p_values]
    bars = ax.bar(index, p_values, bar_width, color=colors, alpha=0.5)
    ax.axhline(y=0.05, color='black', linestyle='--',alpha = 0.5,linewidth = 1,dashes=(8,4))
    if y_lable:
        ax.set_ylabel(y_lable, fontsize=14)
    ax.set_xticks(index)
    ax.set_xticklabels(labels, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    # ax.legend(fontsize=12)
    # ax.set_title(title,fontsize=14)
    ax.text(0.5, -0.1, title, transform=ax.transAxes, ha='center', fontsize=16, va='top')

    # ax.grid(True)  # 添加背景网格

# 绘制每个子图
plot_ax(ax1, p_values_1, '(a) Min_TTC',y_lable='P-values')
plot_ax(ax2, p_values_2, '(b) Steering Angle Std. Dev.')
plot_ax(ax3, p_values_3, '(c) Acceleration Std. Dev.')

plt.tight_layout()  # 优化布局以避免重叠
# plt.show()
plt.savefig('Figure_5.svg')