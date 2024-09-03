import pandas as pd
import os

# 定义输入文件夹的路径
input_dir_path = r'E:\NFB_data_backup\filtered'

# 遍历input_dir_path下的所有子文件夹
for subdir, dirs, files in os.walk(input_dir_path):
    for file in files:
        if "EYE" in file and file.endswith('.csv'):
            # 定义完整的输入文件路径
            input_file_path = os.path.join(subdir, file)
            
            # 加载CSV文件
            data = pd.read_csv(input_file_path)

            # 选择特定的列
            selected_columns = data[['timestamp', 'RightPupilDiameter', 'LeftPupilDiameter']]

            # 计算时间差，并转换为整数毫秒
            base_time = selected_columns['timestamp'].iloc[0]  # 获取第一行的timestamp
            selected_columns['time_ms'] = ((selected_columns['timestamp'] - base_time) * 1000).round().astype(int)

            # 删除time_ms列中的重复项
            final_data = selected_columns.drop_duplicates(subset=['time_ms'])

            # 定义输出文件的路径
            folder_name = os.path.basename(subdir)  
            output_file_path = os.path.join(subdir, f'{folder_name}_eye_data.csv')

            # 保存为新的CSV文件
            final_data.to_csv(output_file_path, index=False)

print("处理完成！")
