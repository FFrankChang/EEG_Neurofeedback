import os
import pandas as pd

# 设置文件夹路径
folder_path = 'path_to_your_folder'

# 获取所有csv文件
files = [f for f in os.listdir(folder_path) if f.endswith('.csv') and 'time' not in f]

# 将文件分为数据文件和标签文件
data_files = [f for f in files if '_data.csv' in f]
label_files = [f.replace('_data', '') for f in data_files]

# 确保两者一一对应
matched_files = [(label, data) for label, data in zip(label_files, data_files) if label in files]

# 遍历匹配的文件对
for label_file, data_file in matched_files:
    # 读取标签文件
    label_path = os.path.join(folder_path, label_file)
    data_path = os.path.join(folder_path, data_file)
    
    label_df = pd.read_csv(label_path)
    data_df = pd.read_csv(data_path)  

    # 检查labels列是否存在
    if 'labels' in label_df.columns:
        # 使用标签文件的labels列作为数据文件的表头
        new_columns = label_df['labels'].values
        if len(new_columns) == data_df.shape[1]:  # 确保列数匹配
            data_df.columns = new_columns
            # 保存修改后的数据文件
            new_data_path = data_path.replace('_data', '_modified_data')
            data_df.to_csv(new_data_path, index=False)
        else:
            print(f"列数不匹配：{data_file}")
    else:
        print(f"未找到labels列：{label_file}")
