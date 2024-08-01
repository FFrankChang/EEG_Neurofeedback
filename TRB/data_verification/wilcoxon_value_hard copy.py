import numpy as np
from scipy.stats import wilcoxon

# 定义数据
data_silence = [6.33, 5.88, 5.79, 8.33, 4.84, 5.67, 11.99, 8.08]
data_feedback = [5.59, 4.36, 4.17, 6.48, 3.77, 4.62, 10.79, 6.98]

# 进行配对Wilcoxon检验
stat, p = wilcoxon(data_silence, data_feedback)

# 打印结果
print(f"Wilcoxon statistic: {stat}")
print(f"P-value: {p}")

