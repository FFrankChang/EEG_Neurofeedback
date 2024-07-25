import os
import shutil

def move_small_csv_files(source_dir, target_dir):
    # 遍历source_dir下的所有文件和目录
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                # 获取文件大小并转换为KB
                file_size_kb = os.path.getsize(file_path) / 1024
                # 检查文件大小是否小于200KB
                if file_size_kb < 200:
                    # 创建目标目录，如果不存在
                    os.makedirs(target_dir, exist_ok=True)
                    # 构建目标文件路径
                    destination_path = os.path.join(target_dir, file)
                    # 移动文件
                    shutil.move(file_path, destination_path)
                    print(f'Moved "{file_path}" to "{destination_path}"')

# 指定源目录和目标目录路径
source_directory = r'F:\NFB_EXP\Exp_V1_data\filtered'
target_directory = r'F:\NFB_EXP\Exp_V1_data\filtered\lessthan200kb'

move_small_csv_files(source_directory, target_directory)
