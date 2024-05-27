import os
import pandas as pd

# 指定需要搜索的文件夹路径
folder_path = 'path/to/your/folder'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if 'time' in filename and filename.endswith('.csv'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        
        # 读取CSV文件，假设文件没有头部信息(header=None)
        df = pd.read_csv(file_path)
        
        # 添加列名 'time'
        df.columns = ['time']
        
        # 保存修改后的CSV文件，覆盖原文件
        df.to_csv(file_path, index=False)

print("所有含'time'的CSV文件已成功添加列名并保存。")
