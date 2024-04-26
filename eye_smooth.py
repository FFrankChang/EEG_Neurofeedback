import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
def load_data(filepath):
    df = pd.read_csv(filepath)
    # 处理StorageTime，新增timestamp列
    df['timestamp'] = df['StorageTime'] / 10000000
    return df

# 平滑数据
def smooth_data(df, window_size=10, use_ewm=False, alpha=0.3):
    if use_ewm:
        # 使用指数移动平均
        df['smoothed_left'] = df['smarteye|LeftPupilDiameter'].ewm(alpha=alpha).mean()
        df['smoothed_right'] = df['smarteye|RightPupilDiameter'].ewm(alpha=alpha).mean()
    else:
        # 使用简单移动平均
        df['smoothed_left'] = df['smarteye|LeftPupilDiameter'].rolling(window=window_size, center=True).mean()
        df['smoothed_right'] = df['smarteye|RightPupilDiameter'].rolling(window=window_size, center=True).mean()
    return df

# 绘制平滑后的瞳孔直径折线图
def plot_pupil_diameters(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['smoothed_left'], label='Smoothed Left Pupil Diameter',linewidth=0.5)
    plt.plot(df['timestamp'], df['smoothed_right'], label='Smoothed Right Pupil Diameter',linewidth=0.5)
    plt.xlabel('Timestamp')
    plt.ylabel('Pupil Diameter')
    plt.title('Smoothed Pupil Diameter Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# 主函数
def main():
    # 修改此路径以指向你的CSV文件位置
    filepath = 'final_eye.csv'
    df = load_data(filepath)
    df = smooth_data(df, window_size=10, use_ewm=True, alpha=0.1)  # 可以调整参数以适应数据
    plot_pupil_diameters(df)

if __name__ == '__main__':
    main()
