import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
def load_data(filepath):
    df = pd.read_csv(filepath)
    # 处理StorageTime，新增timestamp列
    df['timestamp'] = df['StorageTime'] / 10000000
    return df

def plot_pupil_diameters(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['smarteye|LeftPupilDiameter'], label='Left Pupil Diameter',linewidth=0.5)
    plt.plot(df['timestamp'], df['smarteye|RightPupilDiameter'], label='Right Pupil Diameter',linewidth=0.5)
    plt.xlabel('Timestamp')
    plt.ylabel('Pupil Diameter')
    plt.title('Pupil Diameter Over Time')
    plt.legend()
    plt.grid(True)  
    plt.show()

# 主函数
def main():
    filepath = 'final_eye.csv'
    df = load_data(filepath)
    plot_pupil_diameters(df)

if __name__ == '__main__':
    main()
