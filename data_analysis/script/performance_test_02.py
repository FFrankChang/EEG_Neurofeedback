import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

file_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240604\cq_results_abs.csv'
test_data = pd.read_csv(file_path)

# 筛选出场景为“hard”的数据
hard_data = test_data[test_data['scenario'] == 'hard']

# 进一步按 condition 分组
silence_data = hard_data[hard_data['condition'] == 'silence']
feedback_data = hard_data[hard_data['condition'] == 'feedback']

# 提取不同的数据列，假设您的CSV文件的列名遵循以下模式
def extract_data(df, regex):
    return df.filter(regex=regex).stack().reset_index(drop=True)

# 提取 Silence 和 Feedback 的数据
mean_change_rate_silence = extract_data(silence_data, 'Mean Change Rate \d')
mean_change_rate_feedback = extract_data(feedback_data, 'Mean Change Rate \d')
variance_silence = extract_data(silence_data, 'Variance \d')
variance_feedback = extract_data(feedback_data, 'Variance \d')
coefficient_of_variation_silence = extract_data(silence_data, 'Coefficient of Variation \d')
coefficient_of_variation_feedback = extract_data(feedback_data, 'Coefficient of Variation \d')

# 创建一个图形和三个子图
fig, axs = plt.subplots(3, 1, figsize=(12, 18))  # 三个子图，垂直排列

# 绘制 Mean Change Rate
axs[0].plot(mean_change_rate_silence, marker='o', linestyle='-', color='slateblue', label='Silence')
axs[0].plot(mean_change_rate_feedback, marker='o', linestyle='-', color='navy', label='Feedback')
axs[0].set_title('Mean Change Rate for "Hard" Scenario')
axs[0].set_xlabel('Data Point Index')
axs[0].set_ylabel('Mean Change Rate')
axs[0].grid(True)
axs[0].legend()

# 绘制 Variance
axs[1].plot(variance_silence, marker='o', linestyle='-', color='green', label='Silence')
axs[1].plot(variance_feedback, marker='o', linestyle='-', color='darkgreen', label='Feedback')
axs[1].set_title('Variance for "Hard" Scenario')
axs[1].set_xlabel('Data Point Index')
axs[1].set_ylabel('Variance')
axs[1].grid(True)
axs[1].legend()

# 绘制 Coefficient of Variation
axs[2].plot(coefficient_of_variation_silence, marker='o', linestyle='-', color='red', label='Silence')
axs[2].plot(coefficient_of_variation_feedback, marker='o', linestyle='-', color='darkred', label='Feedback')
axs[2].set_title('Coefficient of Variation for "Hard" Scenario')
axs[2].set_xlabel('Data Point Index')
axs[2].set_ylabel('Coefficient of Variation')
axs[2].grid(True)
axs[2].legend()

# 调整子图间距
plt.tight_layout()

# 显示图形
plt.show()
