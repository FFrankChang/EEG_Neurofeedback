import numpy as np
from scipy.stats import wilcoxon

# 模拟数据
data_with_feedback = np.random.normal(loc=0, scale=1, size=30)
data_without_feedback = np.random.normal(loc=0.5, scale=1, size=30)

# 执行Wilcoxon符号秩检验
stat, p = wilcoxon(data_with_feedback, data_without_feedback)

# 输出结果
print("Wilcoxon test statistic:", stat)
print("P-value:", p)
