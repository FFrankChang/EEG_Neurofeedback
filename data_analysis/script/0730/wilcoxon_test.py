import pandas as pd
from scipy.stats import wilcoxon
import numpy as np

# 加载CSV文件
df = pd.read_csv(r"D:\gitee\EEG_Neurofeedback\exp1_results.csv")

# 筛选出scenario为easy的数据
filtered_df = df[df['scenario'] == 'hard']

# 分别获取silence和feedback条件下的Steering_Angle_Std数据
silence_data = filtered_df[filtered_df['condition'] == 'silence']['Steering_Angle_Std'].tolist()
feedback_data = filtered_df[filtered_df['condition'] == 'feedback']['Steering_Angle_Std'].tolist()


stat, p_value = wilcoxon(silence_data, feedback_data)

n = len(silence_data)

# 计算z值和r值
z_value = (stat - (n*(n+1)/4)) / np.sqrt((n*(n+1)*(2*n+1))/24)
r_value = z_value / np.sqrt(n)

print(f'Statistic: {stat}')
print(f'P-value: {p_value}')
print(f'Z-value: {z_value}')
print(f'R-value: {r_value}')