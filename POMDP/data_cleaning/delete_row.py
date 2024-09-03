import pandas as pd

# 加载CSV文件
file_path = r'D:\gitee\EEG_Neurofeedback\POMDP\results\final_results_60s.csv'  # 更改为你的文件路径
df = pd.read_csv(file_path)

# 需要删除的文件名列表
filenames_to_remove = [
    'carla_C01_S01_D01_silence_20240720105253.csv',
    'carla_C01_S01_D02_feedback_20240820203555.csv',
    'carla_C01_S01_D02_silence_20240820203351.csv'
]

# 删除指定的行
df = df[~df['Filename'].isin(filenames_to_remove)]

# 保存更改回原始文件
df.to_csv(file_path, index=False)
