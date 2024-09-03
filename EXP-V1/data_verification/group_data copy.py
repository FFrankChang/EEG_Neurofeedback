import pandas as pd
import numpy as np
import os

# 设置文件夹路径
folder_path = r'E:\NFB_data_backup\results\test_01'

# 为每个 CSV 文件分配标签并保存
def assign_group_and_save(file_path):
    # 读取数据
    data = pd.read_csv(file_path)
    
    # 分配标签的函数
    def assign_group(sub_df):
        shuffled_df = sub_df.sample(frac=1, random_state=42).reset_index(drop=True)
        mid_point = len(shuffled_df) // 2
        shuffled_df['Label'] = ['A'] * mid_point + ['B'] * (len(shuffled_df) - mid_point)
        return shuffled_df

    # 应用分组函数并重置索引
    grouped_data = data.groupby(['Subject', 'Day', 'Condition']).apply(assign_group).reset_index(drop=True)

    # 保存修改后的数据到原文件
    grouped_data.to_csv(file_path, index=False)


# 遍历文件夹中所有的 CSV 文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(f'Processing file: {filename}')
        assign_group_and_save(file_path)
