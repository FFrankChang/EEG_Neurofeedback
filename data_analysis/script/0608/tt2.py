import os
import pandas as pd

def merge_csv_files(folder_path, output_file):
    # 获取指定文件夹内所有CSV文件的路径
    csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # 创建一个空的DataFrame用于存放合并后的数据
    merged_data = pd.DataFrame()
    
    # 逐个读取CSV文件并合并到merged_data DataFrame中
    for file in csv_files:
        data = pd.read_csv(file)
        merged_data = pd.concat([merged_data, data], ignore_index=True)
    
    # 保存合并后的数据到新的CSV文件中
    merged_data.to_csv(output_file, index=False)
    print(f'Merged CSV saved as {output_file}')

# 使用示例
folder_path = r'E:\EEG_Neurofeedback\data_analysis\results\20240606\+3sresults\all'  # 替换为你的CSV文件所在的文件夹路径
output_file = '+3s_result.csv'  # 替换为你想保存的输出文件路径
merge_csv_files(folder_path, output_file)
