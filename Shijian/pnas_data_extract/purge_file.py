import os

def delete_csv_files(folder_path):
    # 获取文件夹中的所有文件名
    all_files = os.listdir(folder_path)
    
    # 找出所有_time.csv和_data.csv文件
    time_files = [f for f in all_files if f.endswith('_time.csv')]
    data_files = [f for f in all_files if f.endswith('_data.csv')]
    
    # 合并两个列表
    files_to_delete = time_files + data_files
    
    for file in files_to_delete:
        file_path = os.path.join(folder_path, file)
        try:
            os.remove(file_path)
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"无法删除文件: {file_path}. 错误: {e}")

# 调用函数，传入文件夹路径
folder_path = 'your_folder_path_here'
delete_csv_files(folder_path)
