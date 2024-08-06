import pandas as pd

# 指定文件路径
file_path = 'D:\\pupil-size-master\\code\\Examples\\Dataset_nfb1\\Results\\Results6_10.csv'
output_path = 'D:\\pupil-size-master\\code\\Examples\\Dataset_nfb1\\Results\\silence\\C02_silence_D01.csv'

# 读取CSV文件
df = pd.read_csv(file_path)

# 筛选行
filtered_df = df[df['segmentName'].str.contains('C02_silence_D01')]

# 保存筛选后的数据到新的CSV文件
filtered_df.to_csv(output_path, index=False)

print("筛选并保存文件完成！")

