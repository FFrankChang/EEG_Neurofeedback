import pandas as pd

# 定义输入和输出文件的路径
input_file_path = r'F:\NFB_EXP\Exp_V1_data\filtered\S07_D03\EYE_20240721171629.csv'
output_file_path = 'eye_data.csv'

# 加载CSV文件
data = pd.read_csv(input_file_path)

# 选择特定的列
selected_columns = data[['timestamp', 'RightPupilDiameter', 'LeftPupilDiameter']]

# 计算时间差，并转换为整数毫秒
base_time = selected_columns['timestamp'].iloc[0]  # 获取第一行的timestamp
selected_columns['time_ms'] = ((selected_columns['timestamp'] - base_time) * 1000).round().astype(int)

# 删除time_ms列中的重复项
final_data = selected_columns.drop_duplicates(subset=['time_ms'])

# 保存为新的CSV文件
final_data.to_csv(output_file_path, index=False)
