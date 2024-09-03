import pandas as pd

# 指定CSV文件的路径
file_path = r'D:\gitee\EEG_Neurofeedback\final_results_60s.csv'

# 读取CSV文件
df = pd.read_csv(file_path)

# 列出需要删除的列
columns_to_drop = ['Average_Lanes_Per_Change', 'Successful_Changes', 'Total_Successful_Change_Time']

# 删除指定的列
df.drop(columns=columns_to_drop, inplace=True)

# 将修改后的DataFrame保存回原文件
df.to_csv(file_path, index=False)

print("Columns removed and file saved successfully.")
