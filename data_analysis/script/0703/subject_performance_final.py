import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载CSV文件
file_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240703\all_modified.csv'
data = pd.read_csv(file_path)
data['Steering_Angle_Std'] = data['Steering_Angle_Std'] * 540
# 过滤 'easy' 和 'hard' 场景的数据
data_easy = data[data['scenario'] == 'easy']
data_hard = data[data['scenario'] == 'hard']

# 设置绘图风格
sns.set(style="whitegrid")

# 定义颜色
palette = {"silence": "grey", "feedback": "lightblue"}

# 字体大小
font_size = 14

# 绘制 'easy' 场景的图
plt.figure(figsize=(12, 6))
barplot = sns.barplot(x='subject', y='Steering_Angle_Std', hue='condition', data=data_easy, palette=palette)
plt.title('Standard Deviation of Steering Angle by Subject and Condition (easy)', fontsize=font_size)
plt.xlabel('Subject', fontsize=font_size)
plt.ylabel('Standard Deviation of Steering Angle', fontsize=font_size)
plt.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=font_size)

# 在柱状图上标出数据
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.3f'),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center', 
                     xytext = (0, 9), 
                     textcoords = 'offset points')

plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.tight_layout()
plt.savefig('steering_angle_easy.png', dpi=300)
plt.show()

# 绘制 'hard' 场景的图
plt.figure(figsize=(12, 6))
barplot = sns.barplot(x='subject', y='Steering_Angle_Std', hue='condition', data=data_hard, palette=palette)
plt.title('Standard Deviation of Steering Angle by Subject and Condition (hard)', fontsize=font_size)
plt.xlabel('Subject', fontsize=font_size)
plt.ylabel('Standard Deviation of Steering Angle', fontsize=font_size)
plt.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=font_size)

# 在柱状图上标出数据
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.3f'),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center', 
                     xytext = (0, 9), 
                     textcoords = 'offset points')

plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.tight_layout()
plt.savefig('steering_angle_hard.png', dpi=300)
plt.show()
