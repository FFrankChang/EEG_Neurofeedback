import pandas as pd
import matplotlib.pyplot as plt
import os

# 指定包含CSV文件的文件夹路径
input_folder_path = r'E:\pre_nfb_raw_data'  # 更改为你的输入文件夹路径

# 指定保存图片的文件夹路径
output_folder_path = r'C:\Users\Lenovo\EEG_Neurofeedback\arousal_results'  # 更改为你的输出文件夹路径

# 设定阈值
threshold = 1 # 更改为适合你数据的阈值

# 确保输出文件夹存在，如果不存在则创建
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

file_index = 0
# 遍历指定文件夹及其子文件夹中的所有文件
for root, dirs, files in os.walk(input_folder_path):
    for file in files:
        if 'psd' in file and file.endswith('.csv'):
            file_path = os.path.join(root, file)
            data = pd.read_csv(file_path)

            # 检查'arousal'列是否存在
            if 'arousal' in data.columns:
                # 应用阈值，生成二进制列
                data['arousal_binary'] = (data['arousal'] > threshold).astype(int)

                plt.figure()  # 创建新的图形，避免重叠
                plt.plot(data['arousal_binary'], color='blue', marker='o', linestyle='-',alpha=0.5)  # 使用折线图表示
                plt.xlabel('Sample Index')
                # plt.ylabel('Arousal Binary Values')
                plt.title(f'MDP Results Over Time')
                plt.grid(True)
                file_index+=1
                # 根据文件夹名称确定保存的文件格式
                if 'silence' in root:
                    format = 'jpg'
                elif 'feedback' in root or True:  # 对于包含'hard'或其他情况
                    format = 'png'
                
                # 构建输出文件路径
                output_file_path = os.path.join(output_folder_path, f'{file_index}_time_series.{format}')

                # 保存图形到指定的输出文件夹
                plt.savefig(output_file_path)
                plt.close()  # 关闭图形，释放内存
            else:
                print(f"文件 '{file}' 中不存在 'arousal' 列。")
