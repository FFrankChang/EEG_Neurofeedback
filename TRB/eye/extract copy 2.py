import os
import pandas as pd

def process_folder(subdirectory):
    data_file = None
    time_file = None

    # 查找包含 'filtered' 和 'results' 的文件
    for file in os.listdir(subdirectory):
        if 'filtered' in file:
            data_file = os.path.join(subdirectory, file)
        elif 'carla_results' in file:
            time_file = os.path.join(subdirectory, file)

    if data_file is None or time_file is None:
        print(f"Missing files in {subdirectory}, skipping...")
        return

    # 加载CSV文件
    data_df = pd.read_csv(data_file)
    time_df = pd.read_csv(time_file)

    def calculate_mean(row):
        mask = (data_df['timestamp'] >= row['TOR Time']) & (data_df['timestamp'] <= row['TOR 30'])
        subset = data_df.loc[mask]
        
        return subset['ZScorePupilDiameter'].mean() if not subset.empty else None

    # 应用函数并创建新列
    time_df['Average_ZScorePupilDiameter'] = time_df.apply(calculate_mean, axis=1)

    # 保存修改后的时间index文件
    updated_time_file = os.path.join(subdirectory, 'updated_' + os.path.basename(time_file))
    time_df.to_csv(updated_time_file, index=False)
    print(f"Updated file saved to {updated_time_file}")

def process_all_subdirectories(main_directory):
    for entry in os.listdir(main_directory):
        subdirectory = os.path.join(main_directory, entry)
        if os.path.isdir(subdirectory):
            print(f"Processing directory: {subdirectory}")
            process_folder(subdirectory)

# 主目录路径
main_directory_path = r'E:\NFB_data_backup\20240730'
process_all_subdirectories(main_directory_path)
