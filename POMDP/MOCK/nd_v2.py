import pandas as pd
import matplotlib.pyplot as plt
import os

# 指定包含CSV文件的文件夹路径
input_folder_path = r'E:\pre_nfb_raw_data'  # 更改为你的输入文件夹路径

# 指定保存图片的文件夹路径
output_folder_path = r'C:\Users\Lenovo\EEG_Neurofeedback\arousal_distribution'  # 更改为你的输出文件夹路径

# 确保输出文件夹存在，如果不存在则创建
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 遍历指定文件夹及其子文件夹中的所有文件
for root, dirs, files in os.walk(input_folder_path):
    for file in files:
        if 'psd' in file and file.endswith('.csv'):
            file_path = os.path.join(root, file)
            data = pd.read_csv(file_path)

            # 检查'arousal'列是否存在
            if 'arousal' in data.columns:
                plt.figure()  # 创建新的图形，避免重叠
                plt.hist(data['arousal'], bins=20, color='blue', alpha=0.7)
                plt.xlabel('Arousal Values')
                plt.ylabel('Frequency')
                plt.title(f'Frequency Distribution of Arousal in {file}')
                plt.grid(True)

                # 根据文件夹名称确定保存的文件格式
                if 'easy' in root:
                    format = 'jpg'
                elif 'hard' in root or True:  # 对于包含'hard'或其他情况
                    format = 'png'
                
                # 构建输出文件路径
                output_file_path = os.path.join(output_folder_path, f'{os.path.splitext(file)[0]}_arousal_histogram.{format}')

                # 保存图形到指定的输出文件夹
                plt.savefig(output_file_path)
                plt.close()  # 关闭图形，释放内存
            else:
                print(f"文件 '{file}' 中不存在 'arousal' 列。")
