import pandas as pd

# 读取CSV文件
file_path = r'D:\pupil-size-master\code\Examples\Dataset_sby\rawData\S03_eye_data_deduplicated.csv'
df = pd.read_csv(file_path)

# 将time_ms列的值除以1000
df['time_ms_div_1000'] = df['time_ms'] / 1000

# 检查除以1000后的time_ms列是否有重复值
duplicated_times = df['time_ms_div_1000'][df['time_ms_div_1000'].duplicated()]

if duplicated_times.empty:
    print("除以1000后的time_ms值没有重复。")
else:
    print("除以1000后的重复的time_ms值如下：")
    print(duplicated_times)


