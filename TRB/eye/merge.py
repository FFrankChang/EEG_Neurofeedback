import pandas as pd
import os

def merge_csv_files(root_dir):
    # 创建一个空的DataFrame用于存放合并后的数据
    merged_data = pd.DataFrame()

    # 遍历root_dir下的所有文件夹和文件
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            # 检查文件名是否包含"updated"且为CSV文件
            if 'updated' in file and file.endswith('.csv'):
                # 构建文件的完整路径
                file_path = os.path.join(subdir, file)
                # 读取CSV文件
                df = pd.read_csv(file_path)
                # 获取文件所在的文件夹名
                folder_name = os.path.basename(subdir)
                # 在DataFrame中添加表示文件夹名的新列
                df['Folder'] = folder_name
                # 将读取的数据加入到合并后的DataFrame中
                merged_data = pd.concat([merged_data, df], ignore_index=True)

    return merged_data

# 调用函数，传入包含CSV文件的根目录路径
root_directory = r'E:\NFB_data_backup\20240730'  # 请替换为您的根目录路径
merged_csv = merge_csv_files(root_directory)

# 如果需要保存合并后的CSV文件
merged_csv.to_csv('eye.csv', index=False)

