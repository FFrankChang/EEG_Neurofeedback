import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create a sample dataset
np.random.seed(0)
data = {
    'Sham': np.random.normal(0.2, 1, 30),
    'BCI': np.random.normal(0.5, 1, 30)
}

# Convert the dictionary into a DataFrame
df = pd.DataFrame(data)

# Plotting the boxplot
plt.figure(figsize=(6, 6))
# Enabling patch_artist to fill with color
boxplot = df.boxplot(column=['Sham', 'BCI'], widths=0.6, patch_artist=True, return_type='dict')
# plt.title('Normalized Pupil Size by Condition', fontsize=14)
plt.ylabel('Normalized pupil size (mm)', fontsize=12)

colors = ['royalblue', 'white']  # Colors for each box
line_colors = ['royalblue', 'black']  # Line colors for each box
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

# Adding comparison lines and text for p-value
def add_comparison_line(group1, group2, text, y, h, text_size=12):
    x1, x2 = group1, group2
    plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=line_colors[group2-1])
    plt.text((x1+x2)*0.5, y+h, text, ha='center', va='bottom', color=line_colors[group2-1], fontsize=text_size)

# Customize y and h to fit your specific data range
y_max = df.max().max() + 0.5
h = 0.1

add_comparison_line(1, 2, 'p=0.011', y_max, h, text_size=12)

plt.show()
