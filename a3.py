import pandas as pd

data1 = pd.read_csv('1.csv')
data2 = pd.read_csv('2.csv')


start_time = max(data1['timestamp'].min(), data2['timestamp'].min())
end_time = min(data1['timestamp'].max(), data2['timestamp'].max())

data1 = data1[(data1['timestamp'] >= start_time) & (data1['timestamp'] <= end_time)]
data2 = data2[(data2['timestamp'] >= start_time) & (data2['timestamp'] <= end_time)]

merged_data = pd.merge_asof(data1, data2, on='timestamp', direction='nearest')

merged_data.to_csv('merged_file2.csv', index=False)

print('文件合并完成，保存为 "merged_file.csv"。')
