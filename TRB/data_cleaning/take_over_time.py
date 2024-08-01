import os
import pandas as pd

def calculate_time_differences(directory):
    results = []
    files = []

    # 获取每个文件的创建时间并排序
    for filename in os.listdir(directory):
        # 检查是否包含“carla”以及“C01”或“C02”
        if 'carla' in filename.lower() and ('C01' in filename or 'C02' in filename):
            file_path = os.path.join(directory, filename)
            files.append((file_path, os.path.getctime(file_path)))

    # 按创建时间排序文件
    files.sort(key=lambda x: x[1], reverse=True)

    # 遍历排序后的文件
    for file_path, _ in files:
        try:
            data = pd.read_csv(file_path)
            # 检测'TOR'列的值
            condition = 'Yes' if 'C01' in os.path.basename(file_path) else True
            tor_indices = data[data['TOR'] == condition].index
            if not tor_indices.empty:
                first_tor_index = tor_indices[0]
                first_tor_time = data.at[first_tor_index, 'timestamp']
                last_time = data.at[data.index[-1], 'timestamp']

                # 计算时间差
                time_difference = (last_time - first_tor_time)
                results.append({
                    'File': os.path.basename(file_path),
                    'Condition': 'C01' if 'C01' in os.path.basename(file_path) else 'C02',
                    'Time Difference': time_difference
                })
        except Exception as e:
            print(f"Error processing file {os.path.basename(file_path)}: {e}")

    # 将结果保存到DataFrame中，并打印
    results_df = pd.DataFrame(results)
    results_df_sorted = results_df.sort_values(by='Time Difference')
    print(results_df_sorted)

# 替换为你的文件夹路径
directory_path = r'E:\NFB_data_backup\20240730\S01_D01'
calculate_time_differences(directory_path)
