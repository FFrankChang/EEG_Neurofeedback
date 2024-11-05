import os
import pandas as pd

def find_small_csv_files(directory, keyword="C04", max_size_kb=40):
    # 存储小于指定大小的文件名、路径和时间戳差
    small_files = []
    
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件是否为CSV且包含关键词
            if file.endswith(".csv") and keyword in file:
                # 获取文件的完整路径
                full_path = os.path.join(root, file)
                # 获取文件大小并转换为KB
                file_size_kb = os.path.getsize(full_path) / 1024
                # 检查文件大小是否小于最大大小
                if file_size_kb < max_size_kb:
                    # 读取CSV文件的timestamp列
                    try:
                        data = pd.read_csv(full_path, usecols=['timestamp'])

                        timestamp_diff = data['timestamp'].iloc[-1] - data['timestamp'].iloc[0]
                        small_files.append((file, full_path, timestamp_diff))
                    except Exception as e:
                        small_files.append((file, full_path, f"Error reading file: {str(e)}"))
    
    return small_files

# 指定要搜索的目录
directory_to_search = r'F:\NFB_EXP\Exp_RT'

# 执行函数并打印结果
result = find_small_csv_files(directory_to_search)
for filename, path, diff in result:
    print(f"File: {filename}, Path: {path}, Timestamp Difference: {diff}")
