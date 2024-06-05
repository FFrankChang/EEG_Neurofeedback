import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 路径和搜索名，您可以根据需要更改这些参数
path = r'D:\gitee\EEG_Neurofeedback\data'
search_name = 'lxk'  # 可配置的搜索名

# 查找所有符合条件的文件夹
folders = []
for root, dirs, files in os.walk(path):
    if search_name in root:
        folders.append(root)

# 读取所有符合条件的文件的arousal数据
data_frames = []
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith('.csv') and 'psd' in file:
            full_path = os.path.join(folder, file)
            df = pd.read_csv(full_path)
            if 'arousal' in df.columns:
                # 可以在这里添加其他需要保留的列，如时间戳或标识符
                data_frames.append(df[['timestamp', 'arousal']])

# 合并所有数据帧以进行归一化
all_arousal_data = pd.concat(data_frames, ignore_index=True)

# 归一化
scaler = MinMaxScaler()
all_arousal_data['normalized_arousal'] = scaler.fit_transform(all_arousal_data[['arousal']])

# 保存为新文件，文件名包括搜索名
output_file = os.path.join(path, f'normalized_arousal_{search_name}.csv')
all_arousal_data.to_csv(output_file, index=False)
