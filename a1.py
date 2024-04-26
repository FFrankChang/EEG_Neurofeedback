import pandas as pd

# 读取两个CSV文件
data1 = pd.read_csv('1.csv')
data2 = pd.read_csv('2.csv')


merged_data = pd.merge(data1, data2, on='timestamp', how='outer')

# 对合并后的数据按时间戳进行排序
merged_data.sort_values('timestamp', inplace=True)

# 保存合并后的数据到新的CSV文件
merged_data.to_csv('merged_file.csv', index=False)

print('文件合并完成，保存为 "merged_file.csv"。')
