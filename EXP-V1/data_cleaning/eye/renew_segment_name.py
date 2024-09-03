import os
import pandas as pd

def update_segmentName(file_path):
    # 只提取文件名，而不包含路径
    filename = os.path.basename(file_path)
    
    # 从文件名中提取如S01这样的部分
    part_to_add = filename.split('_')[0]
    
    # 读取CSV文件
    df = pd.read_csv(file_path)
    
    # 检查是否有 'segmentName' 列
    if 'segmentName' not in df.columns:
        print(f"Error: 'segmentName' column not found in the CSV file {file_path}.")
        return
    
    # 更新 'segmentName' 列
    df['segmentName'] = df['segmentName'].apply(lambda x: f"{x}_{part_to_add}")
    
    # 直接保存更新后的数据到源文件
    df.to_csv(file_path, index=False)
    print(f"Updated CSV has been saved back to {file_path}")

def process_folder(directory):
    # 遍历指定文件夹
    for filename in os.listdir(directory):
        if 'segment' in filename and filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            update_segmentName(file_path)


directory = r'E:\NFB_data_backup\eye_extract'
process_folder(directory)
