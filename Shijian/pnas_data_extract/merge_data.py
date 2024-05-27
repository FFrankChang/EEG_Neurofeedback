import os
import pandas as pd

def merge_csv_files(folder_path):
    # 获取文件夹中的所有文件名
    all_files = os.listdir(folder_path)
    
    # 找出所有_time.csv和_data.csv文件
    time_files = [f for f in all_files if f.endswith('_time.csv')]
    data_files = [f for f in all_files if f.endswith('_data.csv')]
    
    # 以文件名前缀为键创建字典
    time_dict = {os.path.splitext(f)[0].rsplit('_', 1)[0]: f for f in time_files}
    data_dict = {os.path.splitext(f)[0].rsplit('_', 1)[0]: f for f in data_files}
    
    # 找出成对的文件
    common_prefixes = set(time_dict.keys()).intersection(data_dict.keys())
    
    for prefix in common_prefixes:
        time_file_path = os.path.join(folder_path, time_dict[prefix])
        data_file_path = os.path.join(folder_path, data_dict[prefix])
        
        # 读取CSV文件
        time_df = pd.read_csv(time_file_path)
        data_df = pd.read_csv(data_file_path)
        
        # 检查行数是否一致
        if len(time_df) != len(data_df):
            print(f"行数不一致: {time_dict[prefix]} 和 {data_dict[prefix]}")
            continue
        
        # 合并数据
        merged_df = pd.concat([time_df, data_df], axis=1)
        
        # 保存合并后的数据
        merged_file_path = os.path.join(folder_path, f"{prefix}_merged.csv")
        merged_df.to_csv(merged_file_path, index=False)
        print(f"已合并: {merged_file_path}")

# 调用函数，传入文件夹路径
folder_path = 'your_folder_path_here'
merge_csv_files(folder_path)
