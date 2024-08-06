import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('TkAgg')

import numpy as np
import pandas as pd

mpl.rcParams['font.family'] = 'Times New Roman'

data1 = {
    'True Feedback': [0.46,0.81,0.78,0.41,0.73,0.83],
    'Silence': [0.68,0.85,0.84,0.46,0.94,0.86]
}
data2 = {
    'Sham Feedback': [0.94,0.86,0.78,0.81,0.77,0.84],
    'Silence': [0.88,1.09,0.74,0.73,0.33,0.71]
}
data3 = {
    'True Feedback': [0.46,0.81,0.78,0.41,0.73,0.83],
    'Sham Feedback': [0.94,0.86,0.78,0.81,0.77,0.84]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6),sharey=True)  # 三个并列子图

def plot_boxplot(df, ax, title,line_colors=['royalblue', 'dimgray'], type='a',label=None):
    if type == 'a':
        boxplot = df.boxplot(ax=ax, column=['True Feedback', 'Silence'], widths=0.6, patch_artist=True, return_type='dict')
    elif type == 'b':
        boxplot = df.boxplot(ax=ax, column=['Sham Feedback', 'Silence'], widths=0.6, patch_artist=True, return_type='dict')
    elif type == 'c':
        boxplot = df.boxplot(ax=ax, column=['True Feedback', 'Sham Feedback'], widths=0.6, patch_artist=True, return_type='dict')
    ax.text(0.5, -0.1, title, transform=ax.transAxes, ha='center', fontsize=16, va='top')
    for tick in ax.get_xticklabels():
        tick.set_fontsize(14)
    if label:
        ax.set_ylabel('Normalized Pupil Size (mm)', fontsize=14)
    line_colors = line_colors
    for i, color in enumerate(line_colors):
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

        ax.grid(False)
# 绘制三个子图
plot_boxplot(df1, axes[0], '(a) True Feedback and Silence',['royalblue', 'dimgray'],type='a',label=1)
plot_boxplot(df2, axes[1], '(b) Sham Feedback and Silence',['black', 'dimgray'],type='b')
plot_boxplot(df3, axes[2], '(c) True Feedback and Sham Feedback',['royalblue', 'black'],type='c')

def add_comparison_line(ax, group1, group2, text, y, h, text_size=12):
    x1, x2 = group1, group2
    ax.plot([x1, x1, x2, x2], [y, y+0.02, y+0.02, y], lw=1.5, c='black')
    ax.text((x1+x2)*0.5, y+0.02, text, ha='center', va='bottom', color='black', fontsize=text_size)

y_max = max(df1.max().max(), df2.max().max(), df3.max().max()) + 0.1
h = 0.1

add_comparison_line(axes[0], 1, 2, 'p=0.0313', y_max, h, text_size=14)
add_comparison_line(axes[1], 1, 2, 'p=0.3125', y_max, h, text_size=14)
add_comparison_line(axes[2], 1, 2, 'p=0.0915', y_max, h, text_size=14)

# global_min = min(df1.min().min(), df2.min().min(), df3.min().min())
# global_max = max(df1.max().max(), df2.max().max(), df3.max().max())
# for ax in axes:
#     ax.set_ylim(global_min - 0.1, global_max + 2)

plt.subplots_adjust(wspace=0.1)
# plt.show()
plt.savefig('Pupil.svg')