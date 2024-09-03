import pandas as pd
import os

def merge_csv_files_with_filename(folder_path, output_file):
    # 创建一个空的DataFrame来存储合并后的数据
    merged_data = pd.DataFrame()

    # 遍历指定文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件名是否包含'test'并且是CSV文件
        if 'test' in filename and filename.endswith('.csv'):
            # 读取CSV文件
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path)
            # 在数据中添加一个新列，用来存储文件名
            data['Source_File'] = filename
            # 将数据追加到合并后的DataFrame中
            merged_data = pd.concat([merged_data, data], ignore_index=True)

    # 将合并后的数据保存到新的CSV文件
    merged_data.to_csv(output_file, index=False)
    print(f'Merged data saved to {output_file}')

# 使用示例
folder_path = r'D:\gitee\EEG_Neurofeedback\TRB\data_results'  # 替换为你的文件夹路径
output_file = 'merged_data.csv'  # 你想要保存的新文件名
merge_csv_files_with_filename(folder_path, output_file)
