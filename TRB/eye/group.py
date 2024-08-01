import pandas as pd

def calculate_average_and_save(input_csv, output_csv):
    # 读取CSV文件
    df = pd.read_csv(input_csv)

    # 按照'Folder', 'Scene', 'Condition'进行分组
    grouped_df = df.groupby(['Folder', 'Scene', 'Condition'])

    # 计算每个组的'Average_ZScorePupilDiameter'的平均值
    mean_df = grouped_df['Average_ZScorePupilDiameter'].mean().reset_index()

    # 重命名列，以便清楚地表示这是平均值
    mean_df.rename(columns={'Average_ZScorePupilDiameter': 'Mean_ZScorePupilDiameter'}, inplace=True)

    # 保存结果到新的CSV文件
    mean_df.to_csv(output_csv, index=False)

# 调用函数
input_csv_path = r'D:\gitee\EEG_Neurofeedback\TRB\data_results\eye.csv'  # 替换为输入文件的路径
output_csv_path = 'aaaaa.csv'  # 替换为输出文件的路径

calculate_average_and_save(input_csv_path, output_csv_path)
