import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 加载CSV文件
file_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240703\all_modified.csv'
data = pd.read_csv(file_path)
data['Steering_Angle_Std'] = data['Steering_Angle_Std'] * 540

# 设置文件保存路径
folder_path = '/mnt/data/'

# 函数用于创建变化率图表
def create_change_plot(data, scenario, folder_path):
    # 过滤数据以获得特定scenario
    scenario_data = data[data['scenario'] == scenario]
    

    # 准备数据：计算变化率
    pivot_table = scenario_data.pivot_table(index='subject', columns='condition', values='Steering_Angle_Std')
    pivot_table['change_ratio'] = (pivot_table['silence'] - pivot_table['feedback']) / pivot_table['silence']
    mean_change_ratio = pivot_table['change_ratio'].mean()
    plt.figure(figsize=(14, 8))

    # 设定颜色
    colors = pivot_table['change_ratio'].apply(lambda x: 'palegreen' if x >= 0 else 'lightcoral').values

    change_chart = sns.barplot(x=pivot_table.index, y=pivot_table['change_ratio'], palette=colors)

    # 添加数据标签
    for p in change_chart.patches:
        change_chart.annotate(format(p.get_height() * 100, '.2f') + '%', 
                              (p.get_x() + p.get_width() / 2., p.get_height()), 
                              ha='center', va='center', 
                              xytext=(0, 9), 
                              textcoords='offset points',
                              fontsize=12)
    plt.axhline(y=mean_change_ratio, linestyle='--',color = 'black', label=f'Mean: {mean_change_ratio:.2f}')

    plt.title(f'Change Ratio of Steering Angle Std by Subject ({scenario})', fontsize=16)
    plt.xlabel('Subject', fontsize=16)
    plt.ylabel('Change Ratio ((Silence - Feedback) / Silence)', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig( f'change_ratio_{scenario}.png', dpi=300)
    plt.close()

# 创建 'easy' 场景的变化率图表
create_change_plot(data, 'easy', folder_path)

# 创建 'hard' 场景的变化率图表
create_change_plot(data, 'hard', folder_path)
