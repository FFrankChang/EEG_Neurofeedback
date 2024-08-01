import os
import pandas as pd
from datetime import datetime

def calculate_time_differences(subdirectory, output_csv_name):
    results = []
    files = []

    # 获取每个文件的时间戳，并根据时间戳排序
    for filename in os.listdir(subdirectory):
        if 'carla' in filename.lower() and ('C01' in filename or 'C02' in filename):
            # 解析时间戳
            timestamp_str = filename.split('_')[-1].strip('.csv')[0:14]
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
            file_path = os.path.join(subdirectory, filename)
            files.append((file_path, timestamp))

    # 按时间戳排序文件
    files.sort(key=lambda x: x[1])

    # 遍历排序后的文件
    for file_path, timestamp in files:
        try:
            data = pd.read_csv(file_path)
            filename = os.path.basename(file_path)
            # 解析文件名中的条件
            condition = 'silence' if 'silence' in filename else 'feedback'
            scene = 'C01' if 'C01' in filename else 'C02'
            tor_condition = 'Yes' if 'C01' in filename else True
            tor_indices = data[data['TOR'] == tor_condition].index
            if not tor_indices.empty:
                first_tor_index = tor_indices[0]
                first_tor_time = data.at[first_tor_index, 'timestamp']
                last_time = data.at[data.index[-1], 'timestamp']

                # 计算时间差
                time_difference = (last_time - first_tor_time)
                results.append({
                    'File': filename,
                    'Condition': condition,
                    'Scene': scene,
                    'TOR Time': first_tor_time,
                    'TOR 10': min(first_tor_time + 10, last_time),
                    'TOR 20': min(first_tor_time + 20, last_time),
                    'TOR 30': min(first_tor_time + 30, last_time),
                    'TOR 40': min(first_tor_time + 40, last_time),
                    'TOR 50': min(first_tor_time + 50, last_time),
                    'TOR 60': min(first_tor_time + 60, last_time),
                    'Last Time': last_time,
                    'Time Difference': time_difference
                })
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

    # 将结果保存到DataFrame中，然后输出到CSV文件
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(os.path.join(subdirectory, output_csv_name), index=False)
        print(f"Results saved to {os.path.join(subdirectory, output_csv_name)}")
    else:
        print(f"No valid files processed in {subdirectory}")

# 主函数遍历目录并处理每个子目录
def process_all_subdirectories(directory_path, output_csv_name='carla_results.csv'):
    for entry in os.listdir(directory_path):
        subdirectory_path = os.path.join(directory_path, entry)
        if os.path.isdir(subdirectory_path):
            calculate_time_differences(subdirectory_path, output_csv_name)

# 替换为你的文件夹路径
main_directory_path = r'E:\NFB_data_backup\20240730'
process_all_subdirectories(main_directory_path)
