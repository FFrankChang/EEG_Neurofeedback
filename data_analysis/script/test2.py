import pandas as pd
import matplotlib.pyplot as plt

def calculate_arousal_average_and_plot(csv_file):
    # 读取CSV文件
    data = pd.read_csv(csv_file)
    
    # 计算arousal列的平均值
    arousal_average = data['arousal'].mean()
    
    # 绘制arousal的折线图
    plt.figure(figsize=(10, 5))  # 设置图形的大小
    plt.plot(data['timestamp'], data['arousal'], label='Arousal', marker='o')
    plt.title('Arousal Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Arousal Level')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # 旋转横轴标签，便于阅读
    plt.tight_layout()  # 调整布局以防止重叠
    plt.show()
    
    return arousal_average

# 指定CSV文件路径
csv_file_path = 'D:\Frank_Project\EEG_Neurofeedback\data\psd_20240430_145454_pre.csv'

# 调用函数，并获取arousal平均值
average_arousal = calculate_arousal_average_and_plot(csv_file_path)
print("Average arousal value:", average_arousal)
