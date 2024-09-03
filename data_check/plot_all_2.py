import os
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_data(file_path, data, take_over_time, tor_time):
    # 创建三个子图
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    data['relative_time'] = data['timestamp'] - tor_time

    # 绘制第一个图：Steering_Angle 或 Steering
    if 'Steering_Angle' in data.columns:
        column_name = 'Steering_Angle'
        multiplier = 1
    elif 'Steering' in data.columns:
        column_name = 'Steering'
        multiplier = 540

    # 计算累积标准差
    data['cumulative_std'] = data[column_name].expanding(min_periods=1).std()

    axs[0].plot(data['relative_time'], data[column_name] * multiplier, label=column_name)
    axs[0].plot(data['relative_time'], data['cumulative_std'] * multiplier, label='Cumulative Std Dev', linestyle='--')
    axs[0].set_xlabel('relative_time(s)')
    axs[0].set_ylabel(column_name)
    axs[0].set_title(f'{os.path.basename(file_path)} {column_name}')
    axs[0].legend()
    take_over_relative = take_over_time - tor_time

    # 绘制第二个图：Throttle
    if 'Throttle' in data.columns:
        axs[1].plot(data['relative_time'], data['Throttle'], label='Throttle')
        axs[1].set_xlabel('relative_time(s)')
        axs[1].set_ylabel('Throttle')
        axs[1].set_title('Throttle')
        axs[1].set_ylim([-0.1, 1.1])
    
    # 绘制第三个图：Brake
    if 'Brake' in data.columns:
        axs[2].plot(data['relative_time'], data['Brake'], label='Brake')
        axs[2].set_xlabel('relative_time(s)')
        axs[2].set_ylabel('Brake')
        axs[2].set_title('Brake')
        axs[2].set_ylim([-0.1, 1.1])
    
    if pd.notna(take_over_time):
        for ax in axs:
            ax.axvline(x=take_over_relative, color='lightcoral', linestyle='--', label='Take Over Time')
            ax.legend()
            
    if pd.notna(take_over_time):
        data.loc[data['relative_time'] < take_over_relative, ['Throttle', 'Brake']] = 0
        
    # 保存为PNG，使用CSV文件名
    plt.tight_layout()
    plt.savefig(file_path.replace('.csv', '.png'))
    plt.close()

def process_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        results_path = os.path.join(subdir, 'updated_carla_results.csv')
        if os.path.isfile(results_path):
            results_df = pd.read_csv(results_path)
            for idx, row in results_df.iterrows():
                file_name = row.iloc[0]
                file_path = os.path.join(subdir, file_name)
                if os.path.isfile(file_path):
                    data = pd.read_csv(file_path)
                    data = data[(data['timestamp'] >= row['TOR Time']) & (data['timestamp'] <= row['Last Time'])]
                    plot_data(file_path, data, row['take over time'], row['TOR Time'])
                else:
                    print(f"File {file_name} not found in {subdir}.")

root_directory = r'E:\NFB_data_backup\20240730'
process_files(root_directory)
