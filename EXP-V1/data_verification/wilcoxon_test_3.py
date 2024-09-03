import os
import glob
import pandas as pd
from scipy.stats import wilcoxon

# 指定文件夹路径，这里需要根据您的实际情况调整路径
folder_path = r'E:\NFB_data_backup\results\test_01'

# 获取文件夹内所有的CSV文件
csv_files = [f for f in glob.glob(os.path.join(folder_path, '*.csv')) if 'wilcoxon' not in os.path.basename(f)]

# 对每个CSV文件进行处理
for file_path in csv_files:
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
    day_group_combinations = grouped_data[['Condition', 'Group']].drop_duplicates()

    # 对每个Day和Group组合进行处理
    for _, row in day_group_combinations.iterrows():
        Condition = row['Condition']
        group = row['Group']
        data_subset = grouped_data[(grouped_data['Condition'] == Condition) & (grouped_data['Group'] == group)]
        # 遍历列，进行Wilcoxon检验
        for column in columns_to_test:
            D02_scores = data_subset[data_subset['Day'] == 'D02'][column].dropna().values
            D03_scores = data_subset[data_subset['Day'] == 'D03'][column].dropna().values
            
            if len(D02_scores) > 0 and len(D03_scores) > 0:  # 确保有足够的数据进行检验
                stat, p_value = wilcoxon(D03_scores, D02_scores)
                significant = 'yes' if p_value < 0.05 else 'no'
                result = pd.DataFrame({
                    'Condition': [Condition],
                    'Group': [group],
                    'Variable': [column],
                    'Statistic': [stat],
                    'P-value': [p_value],
                    'Significant': [significant]  
                })
                wilcoxon_results = pd.concat([wilcoxon_results, result], ignore_index=True)
    
    # 保存结果到CSV文件，文件名加上'_wilcoxon'
    output_path = file_path.replace('.csv', '_wilcoxon_D2&D3.csv')
    wilcoxon_results.to_csv(output_path, index=False)

    print("Wilcoxon test results saved to:", output_path)
