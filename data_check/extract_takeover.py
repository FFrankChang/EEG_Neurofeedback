import os
import pandas as pd

def load_and_check_files(root_dir):
    # 遍历root_dir下的所有文件夹
    for subdir, dirs, files in os.walk(root_dir):
        # 检查每个子目录中是否有results.csv
        results_path = os.path.join(subdir, 'updated_carla_results.csv')
        if os.path.isfile(results_path):
            # 读取results.csv文件
            results_df = pd.read_csv(results_path)
            # 用于存储时间戳的字典
            timestamp_dict = {}
            
            # 遍历第一列中的每个文件名
            for file_name in results_df.iloc[:,0]:
                file_path = os.path.join(subdir, file_name)
                # 确保文件存在
                if os.path.isfile(file_path):
                    # 加载文件
                    file_df = pd.read_csv(file_path)
                    # 根据文件名判断处理方式
                    if 'C01' in file_name and 'Mode_Switched' in file_df.columns:
                        # 处理C01文件: 找出Mode_Switched为"Yes"的行
                        switched_df = file_df[file_df['Mode_Switched'] == 'Yes']
                        if not switched_df.empty:
                            timestamp_dict[file_name] = switched_df['timestamp'].tolist()[0]
                        else:
                            timestamp_dict[file_name] = None
                    elif 'C02' in file_name and 'Takeover' in file_df.columns:
                        # 处理C02文件: 打印Takeover为True的第一行的时间戳
                        takeover_df = file_df[file_df['Takeover'] == True]
                        if not takeover_df.empty:
                            first_takeover_timestamp = takeover_df.iloc[0]['timestamp']
                            timestamp_dict[file_name] = first_takeover_timestamp
                        else:
                            timestamp_dict[file_name] = None
                    else:
                        timestamp_dict[file_name] = None
                else:
                    print(f"File {file_name} not found in {subdir}.")

            # 更新results_df，添加新列'take over time'
            results_df['take over time'] = results_df.iloc[:,0].map(timestamp_dict)
            # 将更新后的DataFrame写回文件
            results_df.to_csv(results_path, index=False)
            print(f"Updated file saved to {results_path}")

# 指定根目录
root_directory = r'E:\NFB_data_backup\20240730'
load_and_check_files(root_directory)
