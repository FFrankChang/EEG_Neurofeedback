import os

def rename_files(directory):
    # 切换到指定的目录
    os.chdir(directory)
    
    # 遍历目录中的所有文件
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            # 替换文件名中的"SUBJECT"为"krx"
            new_filename = filename.replace("DAY", "D02")
            # new_filename = filename.replace("DAY", "D01")
            # 重命名文件
            os.rename(filename, new_filename)
            print(f'Renamed "{filename}" to "{new_filename}"')

# 指定需要修改文件名的文件夹路径
directory_path = r'F:\NFB_EXP\Exp_V1_data\filtered\lxk_D02'
rename_files(directory_path)
