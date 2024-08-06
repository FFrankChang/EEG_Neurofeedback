import pandas as pd

# 读取CSV文件
file_path = r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\silence\6-10\C02_silence_D01.csv'
data = pd.read_csv(file_path)

# 创建新的DataFrame
new_data = pd.DataFrame()
new_data['meanDiam'] = data['meanPupil_ValidSamples_meanDiam']
new_data['condition'] = 'silence'
new_data['day'] = data['segmentName'].str[-7:-4]  # 提取segmentName列的倒数第5到第7个字符
new_data['sub'] = data['segmentName'].str[-3:]  # 提取segmentName列的最后三个字符

# 保存新的CSV文件
new_file_path = r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\silence\silence\Control_C02_D01.csv'
new_data.to_csv(new_file_path, index=False)
