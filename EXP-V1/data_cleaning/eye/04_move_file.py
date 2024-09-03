import os
import shutil

def find_and_copy_files(source_directory, target_directory):
    # 遍历指定文件夹及其一层子文件夹
    for root, dirs, files in os.walk(source_directory):
        # 只检查一层子文件夹，不深入更多层级
        for dir_name in dirs:
            subfolder_path = os.path.join(root, dir_name)
            for file in os.listdir(subfolder_path):
                # 检查文件名是否符合条件
                if "segment" in file or "eye_data" in file:
                    if file.endswith('.csv'):
                        file_path = os.path.join(subfolder_path, file)
                        # 复制文件到目标文件夹
                        shutil.copy(file_path, target_directory)
                        print(f"已复制: {file_path} 到 {target_directory}")
        break  # 限制遍历到一层子文件夹

# 指定源文件夹和目标文件夹路径
source_directory = r'E:\NFB_data_backup\filtered'
target_directory = r'E:\NFB_data_backup\eye_extract'

# 调用函数
find_and_copy_files(source_directory, target_directory)
