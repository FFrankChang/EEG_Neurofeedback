import pandas as pd
import os

# 指定文件夹路径
folder_path = r'E:\NFB_data_backup\20240730\S04_D01'

# 获取所有包含 "C02" 的 CSV 文件
csv_files = [file for file in os.listdir(folder_path) if 'carla_C02' in file and file.endswith('.csv')]

# 遍历每个文件并计算结果
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path)
    
    # 过滤 TOR 为 True 的数据
    tor_true_data = data[data['TOR'] == True]

    # 计算 "Steering" 列的平均值和标准差
    steering_mean = tor_true_data['Steering'].abs().mean() * 540
    steering_std = tor_true_data['Steering'].abs().std() * 540

    # 打印每个文件的结果
    print(f'文件: {file}')
    print(f'平均值: {steering_mean}')
    print(f'标准差: {steering_std}')
    print('-' * 40)
