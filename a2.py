import pandas as pd

# 读取两个CSV文件
data1 = pd.read_csv('file1.csv')
data2 = pd.read_csv('file2.csv')


# merged_data = pd.merge_asof(data1, data2, on='timestamp')

# 如果需要可以选择使用'nearest'，找到最近的时间戳，无论是前还是后
merged_data = pd.merge_asof(data1, data2, on='timestamp', direction='nearest')

# 可以选择保存合并后的数据到新的CSV文件
merged_data.to_csv('merged_file.csv', index=False)

print('文件合并完成，保存为 "merged_file.csv"。')
