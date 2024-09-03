import os
import pandas as pd

def merge_csv_files(root_folder, output_file):
    # 空的DataFrame用于存储所有数据
    merged_df = pd.DataFrame()

    # 遍历根文件夹
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            # 检查文件名是否包含'results'且是CSV文件
            if 'C02_results' in file and file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                # 读取CSV文件
                df = pd.read_csv(file_path)
                # 将数据追加到merged_df中
                merged_df = pd.concat([merged_df, df], ignore_index=True)

    # 将合并后的数据写入新的CSV文件
    merged_df.to_csv(output_file, index=False)
    print(f'Merged CSV saved as {output_file}')

# 使用示例
root_folder = r'E:\NFB_data_backup\filtered'  # 将此路径替换为实际路径
output_file = 'C02_results.csv'
merge_csv_files(root_folder, output_file)
