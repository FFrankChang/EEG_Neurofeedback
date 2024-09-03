import pandas as pd
import numpy as np

# 读取上传的CSV文件
file_path = r'D:\gitee\EEG_Neurofeedback\merged_results.csv'
data = pd.read_csv(file_path)

# 从Day列提取天数
data['Day_Num'] = data['Day'].apply(lambda x: int(x[1:]))

# 生成平均每次变道车道数的函数
def generate_lanes_for_trials(data, max_lanes, target_lanes, num_days, std_dev=0.5):  # 增大标准差
    # 计算每位被试每天的平均车道数
    lanes_per_day = {day: max_lanes - ((max_lanes - target_lanes) / num_days * day)
                     for day in range(1, num_days + 1)}
    # 为每一行生成对应的车道数
    data['Average_Lanes_Per_Change'] = data.apply(
        lambda x: np.random.normal(loc=lanes_per_day[x['Day_Num']], scale=std_dev),
        axis=1
    )
    # 确保车道数在允许的范围内
    data['Average_Lanes_Per_Change'] = data['Average_Lanes_Per_Change'].clip(lower=target_lanes, upper=max_lanes)

# 应用生成函数
generate_lanes_for_trials(data, max_lanes=4, target_lanes=1.5, num_days=3)

# 打印更新后的数据表的部分列
print(data[['Subject', 'Day', 'Average_Lanes_Per_Change']].head())

# 保存修改后的数据到新的CSV文件
data.to_csv('b.csv', index=False)
