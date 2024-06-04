import os

def rename_folders(directory):
    # 替换规则
    replace_rules = {
        '(silence)': '_silence',
        '(feedback)': '_feedback'
    }
    
    # 列出给定目录下的所有项
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)
        # 确保是一个目录而不是文件
        if os.path.isdir(full_path):
            new_name = name
            # 应用所有替换规则
            for old, new in replace_rules.items():
                new_name = new_name.replace(old, new)
            
            if new_name != name:
                new_path = os.path.join(directory, new_name)
                # 重命名目录
                os.rename(full_path, new_path)
                print(f'Renamed "{name}" to "{new_name}"')


directory_path = r'D:\gitee\EEG_Neurofeedback\data'
rename_folders(directory_path)
