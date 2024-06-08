import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

# 加载数据
data_path = '/mnt/data/output_file_hard.csv'
data = pd.read_csv(data_path)

# 分离每种条件的数据
data_feedback = data[data['condition'] == 'feedback'].set_index('subject')['Steering_Angle_Std']
data_silence = data[data['condition'] == 'silence'].set_index('subject')['Steering_Angle_Std']

# 确保两个数据集按被试者对齐
data_feedback = data_feedback.reindex(data_silence.index)

# 执行Wilcoxon符号秩检验
stat, p = wilcoxon(data_feedback, data_silence)

# 输出结果
print("Wilcoxon test statistic:", stat)
print("P-value:", p)
