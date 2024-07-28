
import pandas as pd
from scipy.stats import wilcoxon

# 路径可能需要根据你的文件位置进行调整
file_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\grouped_expv1_c01_results_e_sham.csv'

# 加载CSV文件
data = pd.read_csv(file_path)

# 筛选Day为D01的数据
data_d01 = data[data['Day'] == 'D01']

# 定义要进行Wilcoxon检验的列
columns_to_test = [
    'Min_TTC', 'Steering_Angle_STD', 'Acceleration_x_Mean',
    'Acceleration_x_STD', 'Acceleration_x_Change_Rate_Mean',
    'Road_Exits', 'Average_Lanes_Per_Change',
    'Successful_Changes', 'Total_Successful_Change_Time'
]

# 创建空DataFrame以存储检验结果
wilcoxon_results = pd.DataFrame(columns=['Variable', 'Statistic', 'P-value', 'Significance'])

# 遍历列，进行Wilcoxon检验
for column in columns_to_test:
    feedback_scores = data_d01[data_d01['Condition'] == 'feedback'][column].values
    silence_scores = data_d01[data_d01['Condition'] == 'silence'][column].values
    stat, p_value = wilcoxon(silence_scores, feedback_scores)
    significance = 'No' if p_value > 0.05 else 'Yes'
    result = pd.DataFrame({
        'Variable': [column],
        'Statistic': [stat],
        'P-value': [p_value],
        'Significance': [significance]
    })
    wilcoxon_results = pd.concat([wilcoxon_results, result], ignore_index=True)

# 保存结果到CSV文件
output_path = 'sham_D01.csv'
wilcoxon_results.to_csv(output_path, index=False)

print("Wilcoxon test results saved to:", output_path)
