import os

def create_nested_folders(base_path):
    # 遍历base_path下的所有文件夹
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):  # 确保它是一个文件夹
            # 在每个文件夹内创建s01和s02
            for subfolder in ['S01', 'S02']:
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)  # 创建子文件夹，如果已存在则不会抛出错误
                # 在s01和s02内创建feedback和silence
                for inner_folder in ['feedback', 'silence']:
                    inner_folder_path = os.path.join(subfolder_path, inner_folder)
                    os.makedirs(inner_folder_path, exist_ok=True)  # 创建更深层的子文件夹

base_path = r'F:\NFB_EXP\Exp_V2_data\finished'

create_nested_folders(base_path)
