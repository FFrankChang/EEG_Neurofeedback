import scipy.stats as stats
import numpy as np

# 定义两组数据
data_silence = [0.58,0.32,0.36,0.4,0.38,0.53]
data_feedback = [0.64,0.66,0.52,0.79,0.47,0.58]

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


stat, p_value = stats.mannwhitneyu(data_feedback, data_silence)


# 打印统计结果
print(f"(U): {stat}")
print(f"P-value: {p_value}")
