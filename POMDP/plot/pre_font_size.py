import matplotlib.pyplot as plt
import numpy as np

# Data extracted from the image
subjects = ['s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10']
silence_values = [0.0106, 0.0077, 0.0069, 0.0123, 0.0100, 0.0145, 0.0102, 0.0054, 0.0291, 0.0208]
feedback_values = [0.0089, 0.0064, 0.0077, 0.0107, 0.0116, 0.0000, 0.0075, 0.0070, 0.0283, 0.0158]
silence_values = [x *540 for x in silence_values]
feedback_values = [x *540 for x in feedback_values]
x = np.arange(len(subjects))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 6))

rects1 = ax.bar(x - width/2, feedback_values, width, label='feedback', color='lightblue')
rects2 = ax.bar(x + width/2, silence_values, width, label='silence', color='grey')

# Adding text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Subject', fontsize=16)
ax.set_ylabel('Steering Angle Std', fontsize=16)
ax.set_title('Steering Angle Std by Subject in Hard Scenario', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(subjects, fontsize=14)
ax.legend(title='Condition', fontsize=14, title_fontsize=16)

# Function to attach a text label above each bar in *rects*, displaying its height.
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14)

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.show()
