import pandas as pd



file_path = r'E:\NFB_data_backup\20240730\S12_D01\EYE_20240730150926.csv'
# 读取CSV文件
df = pd.read_csv(file_path, usecols=['FilteredPupilDiameter', 'timestamp'])

# 计算统计描述
description = df['FilteredPupilDiameter'].describe()
print(description)
# 将统计描述转为DataFrame以便保存
description_df = description.reset_index()
description_df.columns = ['Statistic', 'Value']

# 保存到新的CSV文件
# description_df.to_csv('pupil_statistics.csv', index=False)

print("Statistics saved to pupil_statistics.csv")
