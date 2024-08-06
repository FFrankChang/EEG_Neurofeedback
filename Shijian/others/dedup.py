import pandas as pd

# 加载数据
file_path = r'D:\pupil-size-master\code\Examples\Dataset_sby\rawData\S03_eye_data_deduplicated.csv'  # 修改为您的文件路径
data = pd.read_csv(file_path)

# 将 'time_ms' 列转换为整数
data['time_ms'] = data['time_ms'].astype(int)

# 删除 'time_ms' 列中的重复项，只保留第一个出现的项
data = data.drop_duplicates(subset=['time_ms'], keep='first')

# 保存处理后的数据，如果需要
data.to_csv('S03_eye_data_deduplicated_int.csv', index=False)  # 修改为您想要的输出文件路径

# 打印处理后的数据查看
print(data.head())
