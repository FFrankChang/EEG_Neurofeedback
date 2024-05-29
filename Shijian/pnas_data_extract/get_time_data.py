import os
import h5py
import pandas as pd

# 定义文件夹路径
folder_path = r'E:\Faller_et_al_2019_PNAS_EEG_Neurofeedback_VR_Flight'

# 列出文件夹中所有的.mat文件
mat_files = [f for f in os.listdir(folder_path) if f.endswith('.mat')]

# 遍历所有.mat文件
for mat_file in mat_files:
    # 构建完整的文件路径
    hdf5_file_path = os.path.join(folder_path, mat_file)
    
    # 打开并读取mat文件
    with h5py.File(hdf5_file_path, 'r') as file:
        eeg_data = file['actualVariable']['EEG_full']['times'][:]
    
    # 将数据转换为DataFrame
    eeg_df = pd.DataFrame(eeg_data)
    
    # 构建CSV文件名（原文件名+data）
    csv_file_name = mat_file.replace('.mat', '_time.csv')
    csv_file_path = os.path.join(folder_path, csv_file_name)
    
    # 保存DataFrame到CSV
    eeg_df.to_csv(csv_file_path, index=False)
    
    # 打印保存成功的信息
    print(f"EEG data has been saved to {csv_file_path}")
