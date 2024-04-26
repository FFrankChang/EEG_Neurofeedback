import os
import pandas as pd

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data1_path = os.path.join(base_path, 'data', '1.csv')
data2_path = os.path.join(base_path, 'data', '2.csv')

data1 = pd.read_csv(data1_path)
data2 = pd.read_csv(data2_path)

start_time = max(data1['timestamp'].min(), data2['timestamp'].min())
end_time = min(data1['timestamp'].max(), data2['timestamp'].max())

data1 = data1[(data1['timestamp'] >= start_time) & (data1['timestamp'] <= end_time)]
data2 = data2[(data2['timestamp'] >= start_time) & (data2['timestamp'] <= end_time)]

merged_data = pd.merge_asof(data1, data2, on='timestamp', direction='nearest')

output_path = os.path.join(base_path, 'data', 'merged_file.csv')
merged_data.to_csv(output_path, index=False)

print('文件合并完成，保存为 "merged_file.csv"。')
