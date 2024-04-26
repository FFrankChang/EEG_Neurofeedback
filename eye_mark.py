import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取并处理眼动数据
def load_and_process_eye_data(filepath):
    df = pd.read_csv(filepath)
    df['timestamp'] = df['StorageTime'] / 10000000  # 处理StorageTime生成新的timestamp列
    return df

# 平滑眼动数据
def smooth_pupil_data(df, window_size=10):
    df['smoothed_left'] = df['smarteye|LeftPupilDiameter'].rolling(window=window_size, center=True).mean()
    df['smoothed_right'] = df['smarteye|RightPupilDiameter'].rolling(window=window_size, center=True).mean()
    return df

# 读取模式切换和碰撞数据
def load_mode_and_collision_data(filepath):
    mode_data = pd.read_csv(filepath)
    mode_times = mode_data[mode_data['Mode_Switched'] == 'Yes']['Time'].values
    collision_times = mode_data[mode_data['Collision'] == 'Yes']['Time'].values
    return mode_times, collision_times

# 绘制平滑的瞳孔直径图，并标记模式切换和碰撞事件
def plot_pupil_diameters_with_events(df, mode_times, collision_times):
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['smoothed_left'], label='Smoothed Left Pupil Diameter',linewidth=0.5)
    plt.plot(df['timestamp'], df['smoothed_right'], label='Smoothed Right Pupil Diameter',linewidth=0.5)
    for mode_time in mode_times:
        plt.axvline(x=mode_time, color='lightcoral', linestyle='--', label='Mode Switched' if 'Mode Switched' not in plt.gca().get_legend_handles_labels()[1] else "")
    for collision_time in collision_times:
        plt.axvline(x=collision_time, color='black', linestyle='-.', label='Collision' if 'Collision' not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Pupil Diameter')
    plt.title('Smoothed Pupil Diameter Over Time with Events')
    plt.legend()
    plt.show()

def main():
    eye_data_path = 'final_eye.csv'
    mode_data_path = 'mainvehicle_20240425170754_1_TTC.csv'
    
    eye_data = load_and_process_eye_data(eye_data_path)
    eye_data = smooth_pupil_data(eye_data)
    
    mode_times, collision_times = load_mode_and_collision_data(mode_data_path)
    
    plot_pupil_diameters_with_events(eye_data, mode_times, collision_times)

if __name__ == '__main__':
    main()
