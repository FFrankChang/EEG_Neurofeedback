import pandas as pd

# 加载CSV文件
df = pd.read_csv('/Users/frank/Projects/EEG_Neurofeedback/pointmark_lxk0628.csv')

# 筛选ACTION列为'Takeover'或'Cutin'的数据
filtered_df = df[df['ACTION'].isin(['TAKE_OVER', 'CUT_IN'])]

# 保存筛选后的数据到新的CSV文件
filtered_df.to_csv('event.csv', index=False)
