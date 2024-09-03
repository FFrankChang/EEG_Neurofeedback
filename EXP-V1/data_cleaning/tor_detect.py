

import os
import pandas as pd

def check_and_delete_csv(directory):
    # 遍历目录下的所有文件和文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 确保文件名满足条件：包含 'carla' 和 'C02' 且为CSV文件
            if 'carla' in file.lower() and 'C02' in file and file.endswith('.csv'):
                # 构建完整的文件路径
                file_path = os.path.join(root, file)
                try:
                    # 读取CSV文件
                    data = pd.read_csv(file_path)
                    # 检查'TOR'列是否存在且包含True
                    if 'TOR' in data.columns:
                        if not data['TOR'].any():
                            # 如果TOR列没有True，删除文件
                            os.remove(file_path)
                            print(f"已删除文件 '{file}'，因为'TOR'列中没有True值。")
                    else:
                        print(f"文件 '{file}' 中不存在'TOR'列。")
                except Exception as e:
                    print(f"读取文件 '{file}' 时发生错误: {e}")

# 替换以下路径为你的目标文件夹路径
directory_path = r'E:\NFB_data_backup\filtered'
check_and_delete_csv(directory_path)
