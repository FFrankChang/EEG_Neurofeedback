import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.rcParams['font.family'] = 'Times New Roman'

data2 = {
    'Feedback': [38,48,41,39,35,33],
    'Silence': [46,60,52,45,40,41]
}
data1 = {
    'Feedback': [0.64,0.66,0.52,0.79,0.47,0.58],
    'Silence': [0.58,0.60,0.36,0.66,0.38,0.53]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))  # 两个并列子图

def plot_boxplot(df, ax, title,y_lable):

    boxplot = df.boxplot(ax=ax, column=['Feedback', 'Silence'], widths=0.6, patch_artist=True, return_type='dict')
    # ax.set_title(title, fontsize=16)
    ax.set_ylabel(y_lable, fontsize=14)
    # ax.grid(False) 

    colors = ['royalblue', 'white']  # 每个箱子的颜色
    line_colors = ['royalblue', 'dimgray']  # 每个箱子的线条颜色
    for i, color in enumerate(colors):
        box = boxplot['boxes'][i]
        median = boxplot['medians'][i]
        whiskers = boxplot['whiskers'][i*2:(i+1)*2]
        caps = boxplot['caps'][i*2:(i+1)*2]
        fliers = boxplot['fliers'][i]

        box.set_facecolor("white")
        box.set_linewidth(2)
        box.set_edgecolor(line_colors[i])
        median.set_color(line_colors[i])
        median.set_linewidth(2)

        for whisker in whiskers:
            whisker.set_color(line_colors[i])
            whisker.set_linewidth(2)
        for cap in caps:
            cap.set_color(line_colors[i])
            cap.set_linewidth(2)
        if isinstance(fliers, list):
            for flier in fliers:
                flier.set_marker('o')
                flier.set_markeredgewidth(1)
                fliers.set_markeredgecolor(line_colors[i])
                flier.set_markersize(5)
        else:
            fliers.set_marker('o')
            fliers.set_markeredgewidth(1)
            fliers.set_markersize(5)
            fliers.set_markeredgecolor(line_colors[i])

        y = df.iloc[:, i]
        x = np.random.normal(i + 1, 0.04, size=len(y))
        ax.plot(x, y, 'o', alpha=0.5, markersize=9, color=line_colors[i])
        ax.tick_params(axis='x',labelsize = 14)
        
# 绘制两个子图
plot_boxplot(df1, axes[0], 'A','Min_TTC (s)')
plot_boxplot(df2, axes[1], 'B','Steering Angle Std. Dev. (°)')
# 添加比较线和p值注释的函数
def add_comparison_line(ax, group1, group2, text, y, h, text_size=12,hi=0.3):
    x1, x2 = group1, group2
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='black')
    ax.text((x1+x2)*0.5, y+hi, text, ha='center', va='bottom', color='black', fontsize=text_size)

# 调整y和h以适应特定数据范围
y_max = max(df1.max().max(), df2.max().max()) + 0.5
h = 0.3

# 为每个子图添加比较线和p值
add_comparison_line(axes[0], 1, 2, 'p=0.0313', df1.max().max()+0.05, 0.01, text_size=14,hi=0.01)
add_comparison_line(axes[1], 1, 2, 'p=0.0313', df2.max().max()+0.5, h, text_size=14)


# 调整子图间距
plt.subplots_adjust(wspace=0.2)
plt.show()
