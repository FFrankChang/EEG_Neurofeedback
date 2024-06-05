import os
import pandas as pd

def merge_csv_files(directory, output_file):
    # 初始化一个空的DataFrame来存放合并后的数据
    combined_csv = pd.DataFrame()

    # 遍历目录下的所有文件
    for file in os.listdir(directory):
        # 检查文件名是否包含"results"且为CSV文件
        if "results" in file and file.endswith(".csv"):
            # 构造完整的文件路径
            file_path = os.path.join(directory, file)
            # 读取CSV文件
            df = pd.read_csv(file_path)
            # 将读取的数据追加到总的DataFrame
            combined_csv = pd.concat([combined_csv, df], ignore_index=True)

    # 将合并后的数据保存到新的CSV文件中
    combined_csv.to_csv(output_file, index=False)

# 使用函数
directory = r"D:\gitee\EEG_Neurofeedback\data"  # 替换为你的文件夹路径
output_file = 'all_results.csv'  # 替换为你想保存的文件路径
merge_csv_files(directory, output_file)
