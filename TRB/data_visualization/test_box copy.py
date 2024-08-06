import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.rcParams['font.family'] = 'Times New Roman'

# Create a sample dataset
np.random.seed(0)
data = {
    'Real': [4.58,5.72,8.19,5.36,10.34,7.23],
    'Silence': [3.86,3.77,5.18,4.20,6.63,6.65]
}

# Convert the dictionary into a DataFrame
df = pd.DataFrame(data)

# Plotting the boxplot
plt.figure(figsize=(6, 6))
# Enabling patch_artist to fill with color
boxplot = df.boxplot(column=['Real', 'Silence'], widths=0.6, patch_artist=True, return_type='dict')
plt.ylabel('Normalized pupil size (mm)', fontsize=14)

colors = ['royalblue', 'white']  # Colors for each box
line_colors = ['royalblue', 'dimgray']  # Line colors for each box
for i, color in enumerate(colors):
    box = boxplot['boxes'][i]
    median = boxplot['medians'][i]
    whiskers = boxplot['whiskers'][i*2:(i+1)*2]  # Two whiskers per box
    caps = boxplot['caps'][i*2:(i+1)*2]  # Two caps per box

    box.set_facecolor("white")  # Set the box fill color
    box.set_linewidth(2)      # Set the line width to make the borders bold
    box.set_edgecolor(line_colors[i])  # Set the border color to the chosen line color
    median.set_color(line_colors[i])   # Set the median line color
    median.set_linewidth(2)            # Set the median line width to make it bolder

    # Setting color and width for whiskers and caps
    for whisker in whiskers:
        whisker.set_color(line_colors[i])
        whisker.set_linewidth(2)
    for cap in caps:
        cap.set_color(line_colors[i])
        cap.set_linewidth(2)

# Adding the data points on top of the boxplots
for column_index, column in enumerate(df.columns):
    y = df[column]
    x = np.random.normal(column_index + 1, 0.04, size=len(y))  # Adding some jitter to the x-coordinates for clarity
    plt.plot(x, y, 'o', alpha=0.5, markersize=9, color=line_colors[column_index])  # Match color with box, 'o' for solid circle

# Adding comparison lines and text for p-value
def add_comparison_line(group1, group2, text, y, h, text_size=12):
    x1, x2 = group1, group2
    plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='black')
    plt.text((x1+x2)*0.5, y+h, text, ha='center', va='bottom', color='black', fontsize=text_size)

# Customize y and h to fit your specific data range
y_max = df.max().max()+ 0.5
h = 0.1
plt.tick_params(axis='x', labelsize=14)  # Set x-axis label size

add_comparison_line(1, 2, 'p=0.011', y_max, h, text_size=14)
# plt.grid(False)
plt.show()
