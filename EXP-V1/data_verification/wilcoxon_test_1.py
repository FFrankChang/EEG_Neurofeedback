import pandas as pd
from scipy.stats import wilcoxon
import numpy as np

# 路径可能需要根据你的文件位置进行调整
file_path = r'E:\NFB_data_backup\results\final_results_10s.csv'

# 加载CSV文件
data = pd.read_csv(file_path)

# 按Subject, Day, Condition, 和 Group分组，计算平均值
grouped_data = data.groupby(['Subject', 'Day', 'Condition', 'Group']).agg({
    'Min_TTC': 'mean',
    'Steering_Angle_STD': 'mean',
    'Acceleration_x_Mean': 'mean',
    'Acceleration_x_STD': 'mean',
    'Acceleration_x_Change_Rate_Mean': 'mean',
    'Road_Exits': 'mean',
    'Average_Lanes_Per_Change': 'mean',
    'Successful_Changes': 'mean',
    'Total_Successful_Change_Time': 'mean'
}).reset_index()

# 定义要进行Wilcoxon检验的列
columns_to_test = [
    'Min_TTC', 'Steering_Angle_STD', 'Acceleration_x_Mean',
    'Acceleration_x_STD', 'Acceleration_x_Change_Rate_Mean',
    'Road_Exits', 'Average_Lanes_Per_Change',
    'Successful_Changes', 'Total_Successful_Change_Time'
]

# 创建空DataFrame以存储检验结果
wilcoxon_results = pd.DataFrame()

# 获取所有可能的Day和Group组合
day_group_combinations = grouped_data[['Day', 'Group']].drop_duplicates()

# print(day_group_combinations)

# 对每个Day和Group组合进行处理
for _, row in day_group_combinations.iterrows():
    day = row['Day']
    group = row['Group']
    data_subset = grouped_data[(grouped_data['Day'] == day) & (grouped_data['Group'] == group)]
    # 遍历列，进行Wilcoxon检验
    for column in columns_to_test:
        feedback_scores = data_subset[data_subset['Condition'] == 'feedback'][column].dropna().values
        silence_scores = data_subset[data_subset['Condition'] == 'silence'][column].dropna().values

        # 检查样本大小和零值
        print(f"Testing {column} on Day {day}, Group {group}")
        print("Feedback scores count:", len(feedback_scores), "Zeroes:", np.sum(feedback_scores == 0))
        print("Silence scores count:", len(silence_scores), "Zeroes:", np.sum(silence_scores == 0))

        if len(feedback_scores) > 0 and len(silence_scores) > 0:  # 确保有足够的数据进行检验
            if len(feedback_scores) < 5 or len(silence_scores) < 5:
                print("Warning: Not enough samples for a reliable test.")
            try:
                stat, p_value = wilcoxon(silence_scores, feedback_scores)
                result = pd.DataFrame({
                    'Day': [day],
                    'Group': [group],
                    'Variable': [column],
                    'Statistic': [stat],
                    'P-value': [p_value]
                })
                wilcoxon_results = pd.concat([wilcoxon_results, result], ignore_index=True)
            except Exception as e:
                print("Error during Wilcoxon test:", e)
                
# 保存结果到CSV文件
output_path = 'sham_learning_results.csv'
wilcoxon_results.to_csv(output_path, index=False)

print("Wilcoxon test results saved to:", output_path)
