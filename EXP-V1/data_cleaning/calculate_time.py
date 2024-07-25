import pandas as pd

# 加载CSV文件
file_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\eye_data.csv'
data = pd.read_csv(file_path)

# 计算时间差
base_time = data['timestamp'].iloc[0]  # 获取第一行的timestamp
data['time_ms'] = (data['timestamp'] - base_time) * 1000  # 计算时间差，并转换为毫秒

# 保存为新的CSV文件
new_file_path = 'updated_eye_data.csv'
data.to_csv(new_file_path, index=False)
