import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

# 加载CSV文件
df = pd.read_csv(r'D:\gitee\EEG_Neurofeedback\exp1_results copy.csv')

# 筛选出scenario为easy的数据
filtered_df = df[df['scenario'] == 'easy']

# 获取silence和feedback条件下的Steering_Angle_Std数据
silence_data = filtered_df[filtered_df['condition'] == 'silence']['Steering_Angle_Std'].tolist()
feedback_data = filtered_df[filtered_df['condition'] == 'feedback']['Steering_Angle_Std'].tolist()

# 执行Wilcoxon符号秩检验
stat, p_value = wilcoxon(silence_data, feedback_data)

# 绘制箱线图
plt.figure(figsize=(6, 6))
box = plt.boxplot([silence_data, feedback_data], labels=['Silence', 'Feedback'],
                  patch_artist=True,  # 添加填充色
                  boxprops=dict(facecolor='lightblue'),  # 设置箱体颜色
                  medianprops=dict(color='black'))  # 设置中位线颜色

# 分别设置每个箱子的颜色
box['boxes'][0].set_facecolor('lightcoral')  # Silence的颜色
box['boxes'][1].set_facecolor('lightblue')  # Feedback的颜色

plt.title('Steering Angle Standard Deviation Comparison')
plt.ylabel('Steering Angle Std')

# 在箱型图之间标注p值
plt.text(1.5, max(max(silence_data), max(feedback_data)), f'p={p_value:.4f}', ha='center')

# 显示图表
plt.show()
