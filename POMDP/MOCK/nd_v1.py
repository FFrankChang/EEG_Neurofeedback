import pandas as pd
import matplotlib.pyplot as plt

# 加载CSV文件
file_path = r'E:\pre_nfb_raw_data\20240531_cq_08_hard_silence\psd_20240531_221731_final.csv'  # 更改为你的CSV文件路径
data = pd.read_csv(file_path)

# 确保'arousal'列存在
if 'arousal' in data.columns:
    # 绘制'arousal'数据的频率分布直方图
    plt.hist(data['arousal'], bins=20, color='blue', alpha=0.7)
    plt.xlabel('Arousal Values')
    plt.ylabel('Frequency')
    plt.title('Frequency Distribution of Arousal')
    plt.grid(True)
    plt.show()
else:
    print("CSV文件中不存在 'arousal' 列，请检查列名是否正确。")
