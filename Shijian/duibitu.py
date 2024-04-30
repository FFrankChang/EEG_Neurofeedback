
# import pandas as pd

# # 读取两个CSV文件
# df_every_channel = pd.read_csv('processed_data_every_channel.csv')
# df = pd.read_csv('processed_data.csv')

# # 检查两个文件的行数是否相同
# if len(df_every_channel) != len(df):
#     print("警告：两个文件的行数不相同，替换可能会导致数据对不齐。")
# else:
#     # 替换timestamp列
#     df_every_channel['timestamp'] = df['timestamp']

#     # 保存修改后的文件
#     df_every_channel.to_csv('processed_data_every_channel_modified.csv', index=False)
#     print("文件已成功修改并保存。")

import pandas as pd
import matplotlib.pyplot as plt

# 加载数据
df_every_channel = pd.read_csv("processed_data_every_channel_modified.csv")
df_overall = pd.read_csv("processed_data.csv")

# 假设 'processed_data.csv' 中的 arousal 值在列名为 'arousal'
# 假设 'processed_data_every_channel_modified.csv' 包含时间戳和每个通道的 arousal 值

# 设置绘图
plt.figure(figsize=(12, 8))

# 绘制每个通道的 arousal 值
for column in df_every_channel.columns[1:]:  # 跳过时间戳列
    plt.plot(df_every_channel['timestamp'], df_every_channel[column], label=column)

# 绘制总体 arousal 值
plt.plot(df_overall['timestamp'], df_overall['arousal'], label='Overall Arousal', color='black', linewidth=2)

# 设置图例位置在右侧
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# 设置标题和坐标轴标签
plt.title('Arousal Values Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Arousal')

# 调整图表布局以适应图例
plt.tight_layout()

# 显示图表 
plt.show()



