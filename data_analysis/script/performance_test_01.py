import pandas as pd
import matplotlib.pyplot as plt

file_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240604\cq_results_abs.csv'
test_data = pd.read_csv(file_path)
scenario = 'hard'
# 筛选出场景为“hard”的数据
# hard_data = test_data[test_data['scenario'] == scenario]
hard_data = test_data

# 提取不同的数据列
mean_change_rate = hard_data.filter(regex='Mean Change Rate \d')  # 假设列标题格式是这样的
variance = hard_data.filter(regex='Variance \d')  # 假设列标题格式是这样的
coefficient_of_variation = hard_data.filter(regex='Coefficient of Variation \d')  # 假设列标题格式是这样的

# 将每个数据序列重塑为单列
mean_change_rate_reshaped = mean_change_rate.stack().reset_index(drop=True)
variance_reshaped = variance.stack().reset_index(drop=True)
coefficient_of_variation_reshaped = coefficient_of_variation.stack().reset_index(drop=True)

# 创建一个图形和三个子图
fig, axs = plt.subplots(3, 1, figsize=(12, 12))  # 三个子图，垂直排列

# 绘制 Mean Change Rate
axs[0].plot(mean_change_rate_reshaped, marker='o', linestyle='-', color='slateblue')
axs[0].set_title(f'Mean Change Rate for "{scenario}" Scenario')
axs[0].set_xlabel('Data Point Index')
axs[0].set_ylabel('Mean Change Rate')
axs[0].grid(True)

# 绘制 Variance
axs[1].plot(variance_reshaped, marker='o', linestyle='-', color='gold')
axs[1].set_title(f'Variance for "{scenario}" Scenario')
axs[1].set_xlabel('Data Point Index')
axs[1].set_ylabel('Variance')
axs[1].grid(True)

# 绘制 Coefficient of Variation
axs[2].plot(coefficient_of_variation_reshaped, marker='o', linestyle='-', color='lightcoral')
axs[2].set_title(f'Coefficient of Variation for "{scenario} Scenario')
axs[2].set_xlabel('Data Point Index')
axs[2].set_ylabel('Coefficient of Variation')
axs[2].grid(True)

# 调整子图间距
plt.tight_layout()

# 显示图形
plt.show()
