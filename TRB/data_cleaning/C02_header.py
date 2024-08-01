import os
import pandas as pd

def rename_column_in_csv(folder_path):
    # 遍历文件夹下的所有子文件夹
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件名是否包含'C02'并且是CSV文件
            if 'C02' in file and file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                # 读取CSV文件
                df = pd.read_csv(file_path)
                # 重命名列
                if 'Time' in df.columns:
                    df.rename(columns={'Time': 'timestamp'}, inplace=True)
                    # 保存修改后的文件
                    df.to_csv(file_path, index=False)
                    print(f"Updated file: {file_path}")
                else:
                    print(f"No 'Time' column in {file_path}")

# 使用示例
folder_path = r'E:\NFB_data_backup\20240730'  # 替换为你的文件夹路径
rename_column_in_csv(folder_path)
