import pandas as pd
from datetime import datetime
import os

# 基本路径
base_path = r'D:\Frank_Project\EEG_Neurofeedback\data'

# 日期
date_prefix = "20240523"

# 获取所有会话目录
session_dirs = next(os.walk(base_path))[1]

# 过滤出日期前缀匹配的目录
session_labels = [dir_name for dir_name in session_dirs if dir_name.startswith(date_prefix)]

# 使用列表推导生成文件路径
file_paths = []
for label in session_labels:
    # 构造当前会话的完整路径
    session_path = os.path.join(base_path, label)
    # 读取会话文件夹中所有文件
    for file_name in os.listdir(session_path):
        # 只处理以 "psd" 开头且以 "_final.csv" 结尾的CSV文件
        if file_name.startswith('psd') and file_name.endswith('_final.csv'):
            file_paths.append(os.path.join(session_path, file_name))

# 遍历文件
for file_path in file_paths:
    # 读取CSV文件的第一行和最后一行
    df = pd.read_csv(file_path)
    first_row = df.iloc[0]
    last_row = df.iloc[-1]
    
    # 假设时间戳在 'timestamp' 列
    first_timestamp = first_row['timestamp']
    last_timestamp = last_row['timestamp']
    
    # 判断时间戳类型并转换
    if isinstance(first_timestamp, str):
        first_datetime = datetime.strptime(first_timestamp, '%Y-%m-%d %H:%M:%S')
        last_datetime = datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S')
    else:  # 处理 Unix 时间戳
        # 如果时间戳是毫秒级，先转换为秒
        if first_timestamp > 1e10:  # 大于 10 亿的时间戳可能是毫秒级
            first_timestamp /= 1000
            last_timestamp /= 1000
        first_datetime = datetime.fromtimestamp(first_timestamp)
        last_datetime = datetime.fromtimestamp(last_timestamp)
    
    # 输出结果
    print(f'File: {file_path}')
    print(f'First timestamp: {first_datetime}')
    print(f'Last timestamp: {last_datetime}')
    print('---')


