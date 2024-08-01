import scipy.stats as stats
import numpy as np

# 定义两组数据
data_silence = [6.33,5.88,5.79,8.33,4.84,5.67,11.99,8.08]
data_feedback = [5.59,4.36,4.17,6.48,3.77,4.62,10.79,6.98]

n = len(data_feedback)
# 计算每组数据的均值
mean_feedback = np.mean(data_feedback)
mean_silence = np.mean(data_silence)

# 计算每组数据的标准差
std_real = np.std(data_feedback, ddof=1)  # 采用无偏估计（样本标准差）
std_silence = np.std(data_silence, ddof=1)

print(f"Mean of ‘Feedback’ data: {mean_feedback:.2f}")
print(f"Standard Deviation of ‘Feedback’ data: {std_real:.2f}")
print(f"Mean of 'Silence' data: {mean_silence:.2f}")
print(f"Standard Deviation of 'Silence' data: {std_silence:.2f}")


stat, p_value = stats.wilcoxon(data_silence, data_feedback)

# 计算Z值
z = (stat - n*(n+1)/4) / np.sqrt(n*(n+1)*(2*n+1)/24)

# 计算效应量r
r = z / np.sqrt(n)

# 打印统计结果
print(f"Wilcoxon test statistic (W): {stat}")
print(f"Z-value: {z}")
print(f"r-value: {r}")
print(f"P-value: {p_value}")
