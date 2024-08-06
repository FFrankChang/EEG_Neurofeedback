import pandas as pd

# 载入数据
df = pd.read_csv("D:\\pupil-size-master\\code\\Examples\\Dataset_nfb1\\Results\\C02\\Results1_5_C02_D01.csv")

# 选择指定列并作为第一列
df = df[['meanPupil_ValidSamples_meanDiam']]

# 添加condition列，所有值为'feedback'
df['condition'] = 'feedback'

# ay列
df['day'] = 'D01'

# 保存修改后的文件（如果需要的话）
df.to_csv("D:\\pupil-size-master\\code\\Examples\\Dataset_nfb1\\Results\\C02\\C02_feedback_D01.csv", index=False)
