import pandas as pd
import os
import glob
from datetime import datetime, timedelta

def convert_utc_to_beijing(date_str):
    dt_utc = datetime.strptime(date_str[:-3], "%Y-%m-%d %H:%M:%S.%f")
    dt_beijing = dt_utc + timedelta(hours=8)
    timestamp = dt_beijing.timestamp() + float(date_str[-3:]) * 1e-9
    return timestamp

def process_csv(file_path):
    data = pd.read_csv(file_path)
    
    if 'timestamp' in data.columns:
        data['timestamp'] = data['timestamp'].apply(convert_utc_to_beijing)
        data.to_csv(file_path, index=False)
        print(f"文件已更新并保存回原文件: {file_path}")
    else:
        print(f"错误：文件'{file_path}'中不存在'timestamp'列。")

def process_directory(directory):
    pattern = os.path.join(directory, '**/*carla*C02*.csv')
    files = glob.glob(pattern, recursive=True)
    if not files:
        print("没有找到匹配的文件。")
        return
    for file_path in files:
        process_csv(file_path)

# 指定顶级目录路径
top_directory = r'E:\NFB_data_backup\filtered'  # 请根据需要修改这个路径
process_directory(top_directory)
