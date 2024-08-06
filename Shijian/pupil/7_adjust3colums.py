import pandas as pd

# 加载CSV文件
file_path = r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\C02.csv'  # 替换为你的文件路径
data = pd.read_csv(file_path)

# 删除第一列并将第五列移到第一列位置
data_modified = data.drop(data.columns[0], axis=1)  # 删除第一列
column_names = data_modified.columns.tolist()
fifth_column = column_names.pop(4)  # 取出第五列
column_names.insert(0, fifth_column)  # 将第五列插入到第一列位置
data_final = data_modified.reindex(columns=column_names)

# 删除'sub'列并只保留前三列
data_reduced = data_final.drop('sub', axis=1).iloc[:, :3]

# 保存修改后的文件
output_file_path = r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\C02_update.csv'  # 替换为你想保存的文件路径
data_reduced.to_csv(output_file_path, index=False)
