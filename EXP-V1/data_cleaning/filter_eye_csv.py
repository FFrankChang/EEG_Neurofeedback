import pandas as pd

# 加载CSV文件
file_path = r'F:\NFB_EXP\Exp_V1_data\filtered\syh_D03\EYE_20240721091009.csv'
data = pd.read_csv(file_path)

# 选择特定的列
selected_columns = data[['timestamp', 'RightPupilDiameter', 'LeftPupilDiameter']]

# 保存为新的CSV文件
new_file_path = 'eye_data.csv'
selected_columns.to_csv(new_file_path, index=False)
