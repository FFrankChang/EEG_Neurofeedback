
import pandas as pd

# 定义文件路径和需要读取的行数范围
files_and_rows = [
    (r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\filtered\C02_NFB_D01_max.csv', (0, 10)),  # 读取前17行，包括标题
    (r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\filtered\C02_Control_D01_max.csv', (0, 10)),     # 从第2行到第17行
    (r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\filtered\C02_NFB_D02_max.csv', (0, 10)),
    (r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\filtered\C02_Control_D02_max.csv', (0, 10))
]

# 使用列表推导式和pandas读取指定的行数
combined_data = pd.concat([pd.read_csv(file, skiprows=range(1, start + 1), nrows=end - start) for file, (start, end) in files_and_rows])

# 保存合并后的数据到新的CSV文件
combined_data.to_csv(r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\C02_max.csv', index=False)
