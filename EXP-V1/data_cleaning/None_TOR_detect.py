import os
import pandas as pd

def find_csv_files(directory):
    # 遍历文件夹和子文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 确保文件名符合条件
            if "carla" in file.lower() and "C01" in file and file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    # 读取CSV文件
                    data = pd.read_csv(file_path)
                    # 检查'TOR'列是否存在且不含有'Yes'
                    if 'TOR' in data.columns and not any(data['TOR'] == 'Yes'):
                        print(f"文件名: {file}")
                        print(f"路径: {file_path}")
                except Exception as e:
                    print(f"读取或处理文件 {file_path} 时发生错误: {e}")

# 指定要检查的根目录
directory = r'E:\NFB_data_backup\filtered'
find_csv_files(directory)
