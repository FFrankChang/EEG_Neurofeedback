import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import scipy.stats as stats

mpl.rcParams['font.family'] = 'Times New Roman'

data = {
    'Feedback': [3.79,3.71,5.09,4.57,6.76,6.91],
    'Silence': [3.96,5.30,6.69,5.89,9,7.18]
}

# Convert the dictionary into a DataFrame
df = pd.DataFrame(data)

# Plotting the boxplot
plt.figure(figsize=(6, 6))
# Enabling patch_artist to fill with color
boxplot = df.boxplot(column=['Feedback', 'Silence'], widths=0.6, patch_artist=True, return_type='dict')
plt.ylabel('Steering Angle Std. Dev. (°)', fontsize=14)

line_colors = ['black', 'dimgray']  # Line colors for each box
for i, color in enumerate(line_colors):
    box = boxplot['boxes'][i]
    median = boxplot['medians'][i]
    whiskers = boxplot['whiskers'][i*2:(i+1)*2]  # Two whiskers per box
    caps = boxplot['caps'][i*2:(i+1)*2]  # Two caps per box

    box.set_facecolor("white")  # Set the box fill color
    box.set_linewidth(2)      # Set the line width to make the borders bold
    box.set_edgecolor(line_colors[i])  # Set the border color to the chosen line color
    median.set_color(line_colors[i])   # Set the median line color
    median.set_linewidth(2)            # Set the median line width to make it bolder
    fliers = boxplot['fliers'][i]

    # Setting color and width for whiskers and caps
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

# Adding comparison lines and text for p-value
def add_comparison_line(group1, group2, text, y, h, text_size=12):
    x1, x2 = group1, group2
    plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='black')
    plt.text((x1+x2)*0.5, y+h, text, ha='center', va='bottom', color='black', fontsize=text_size)

# Customize y and h to fit your specific data range
y_max = df.max().max()+ 0.5
h = 0.1
plt.tick_params(axis='x', labelsize=14)  # Set x-axis label size

add_comparison_line(1, 2, 'p=0.0313', y_max, h, text_size=14)

data_feedback = data['Feedback']
data_silence = data['Silence']

n = len(data_feedback)

mean_feedback = np.mean(data_feedback)
mean_silence = np.mean(data_silence)

std_Feedback = np.std(data_feedback, ddof=1)  # 采用无偏估计（样本标准差）
std_silence = np.std(data_silence, ddof=1)
effect = (mean_silence-mean_feedback) / mean_silence * 100
print(f"Mean of ‘Feedback’ data: {mean_feedback:.2f}")
print(f"SD of ‘Feedback’ data: {std_Feedback:.2f}")
print(f"Mean of 'Silence' data: {mean_silence:.2f}")
print(f"SD 'Silence' data: {std_silence:.2f}")

stat, p_value = stats.wilcoxon(data_silence, data_feedback)

print(f"W {stat}")
print(f"P-value: {p_value}")
print(f"Effect: {effect}")
plt.grid(False)
# plt.show()
plt.savefig('Figure_7.svg')