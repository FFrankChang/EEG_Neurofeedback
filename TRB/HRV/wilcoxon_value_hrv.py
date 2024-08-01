import scipy.stats as stats
import numpy as np

# 定义两组数据
data_silence = [26,40,42,30,22.8,58.4]
data_feedback = [13,35,43,26,17.7,52]

n = len(data_feedback)

mean_feedback = np.mean(data_feedback)
mean_silence = np.mean(data_silence)

std_real = np.std(data_feedback, ddof=1)  # 采用无偏估计（样本标准差）
std_silence = np.std(data_silence, ddof=1)

print(f"Mean of ‘Feedback’ data: {mean_feedback:.2f}")
print(f"Standard Deviation of ‘Feedback’ data: {std_real:.2f}")
print(f"Mean of 'Silence' data: {mean_silence:.2f}")
print(f"Standard Deviation of 'Silence' data: {std_silence:.2f}")

stat, p_value = stats.wilcoxon(data_silence, data_feedback)

print(f"Wilcoxon test statistic (W): {stat}")

print(f"P-value: {p_value}")
