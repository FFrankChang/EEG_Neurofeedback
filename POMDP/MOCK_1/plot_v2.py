import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 假设transition_df已经按照之前的代码生成
transition_df = pd.DataFrame({
    'from_state': ['optimal', 'optimal', 'other', 'other', 'optimal', 'optimal', 'other', 'other'],
    'action': [0, 1, 0, 1, 0, 1, 0, 1],
    'to_state': ['optimal', 'other', 'optimal', 'other', 'other', 'optimal', 'other', 'optimal'],
    'probability': [0.7, 0.3, 0.4, 0.6, 0.2, 0.8, 0.3, 0.7]
})

# 将数据按动作分类并创建pivot表
transition_pivot0 = transition_df[transition_df['action'] == 0].pivot_table(index='from_state', columns='to_state', values='probability', fill_value=0)
transition_pivot1 = transition_df[transition_df['action'] == 1].pivot_table(index='from_state', columns='to_state', values='probability', fill_value=0)

# 设置子图布局
fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# 绘制第一个动作（action 0）的状态转移概率热图
sns.heatmap(transition_pivot0, annot=True, cmap='coolwarm', linewidths=.5, ax=axs[0])
axs[0].set_title('Transition Probabilities for Action 0')
axs[0].set_ylabel('From State')
axs[0].set_xlabel('To State')

# 绘制第二个动作（action 1）的状态转移概率热图
sns.heatmap(transition_pivot1, annot=True, cmap='coolwarm', linewidths=.5, ax=axs[1])
axs[1].set_title('Transition Probabilities for Action 1')
axs[1].set_xlabel('To State')

plt.tight_layout()  # 调整布局以防止重叠
plt.show()
