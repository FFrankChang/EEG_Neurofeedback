import os
import pandas as pd

def update_reaction_time(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'updated_carla_results.csv':
                # 读取CSV文件
                file_path = os.path.join(root, file)
                data = pd.read_csv(file_path)

                # 确保必要的列存在
                if 'take over time' in data.columns and 'TOR Time' in data.columns:
                    # 计算反应时间
                    data['reaction time'] = data['take over time'] - data['TOR Time']

                    # 保存更新后的CSV文件
                    data.to_csv(file_path, index=False)
                else:
                    print(f"Missing required columns in {file_path}")

# 调用函数，需要提供文件夹路径
update_reaction_time(r'E:\NFB_data_backup\20240730')
