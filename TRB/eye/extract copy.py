import pandas as pd
import os
from scipy.stats import zscore

# 设置数据文件夹路径
data_dir = r'E:\NFB_data_backup\20240730'

# 遍历目录中的所有文件
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if 'EYE' in file and file.endswith('.csv'):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path, usecols=['FilteredPupilDiameter', 'timestamp'])

            # 过滤数据
            filtered_df = df[df['FilteredPupilDiameter'] >= 0.001]

            # 进行z-score标准化
            filtered_df['ZScorePupilDiameter'] = zscore(filtered_df['FilteredPupilDiameter'])

            # 构建新的文件名
            base_name, extension = os.path.splitext(file)
            new_filename = f'{base_name}_filtered{extension}'
            new_file_path = os.path.join(root, new_filename)

            # 保存过滤和标准化后的数据到相同位置
            filtered_df.to_csv(new_file_path, index=False)
            print(f"Filtered and normalized data saved to {new_file_path}")
