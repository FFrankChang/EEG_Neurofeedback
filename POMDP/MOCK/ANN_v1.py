import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 设置随机种子以复现结果
np.random.seed(42)

# 生成模拟数据
n_samples = 5000
arousal = np.random.uniform(0, 1, n_samples)
workload = np.random.uniform(0, 1, n_samples)
fatigue = np.random.uniform(0, 1, n_samples)
attention = np.random.uniform(0, 1, n_samples)
action = np.random.choice([0, 1], n_samples)  # 0 for Silence, 1 for Feedback

# 定义行动的效应大小
effect_a = 0.1   # Arousal 增加的基本量
effect_w = -0.05 # Workload 减少的基本量
effect_f = 0.03  # Fatigue 增加的基本量
effect_att = -0.02 # Attention 减少的基本量

# 生成下一个时间点的状态
arousal_next = arousal + effect_a * action + np.random.normal(0, 0.1, n_samples)
workload_next = workload + effect_w * action + np.random.normal(0, 0.1, n_samples)
fatigue_next = fatigue + effect_f * action + np.random.normal(0, 0.1, n_samples)
attention_next = attention + effect_att * action + np.random.normal(0, 0.1, n_samples)

# 组装成 DataFrame
data = pd.DataFrame({
    'Arousal': arousal,
    'Workload': workload,
    'Fatigue': fatigue,
    'Attention': attention,
    'Action': action,
    'Arousal_Next': arousal_next,
    'Workload_Next': workload_next,
    'Fatigue_Next': fatigue_next,
    'Attention_Next': attention_next
})

# 划分训练集和测试集
features = data[['Arousal', 'Workload', 'Fatigue', 'Attention', 'Action']]
targets = data[['Arousal_Next', 'Workload_Next', 'Fatigue_Next', 'Attention_Next']]
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# 构建神经网络模型
model = MLPRegressor(hidden_layer_sizes=(10, 10), activation='relu', max_iter=500, random_state=42)
model.fit(X_train, y_train)

# 评估模型
score = model.score(X_test, y_test)
print(f"Model R^2 Score: {score}")

# 可视化预测与实际数据对比
y_pred = model.predict(X_test)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
axes = axes.flatten()
states = ['Arousal', 'Workload', 'Fatigue', 'Attention']
for i, ax in enumerate(axes):
    ax.scatter(y_test.iloc[:, i], y_pred[:, i], alpha=0.3)
    ax.set_xlabel('True Values')
    ax.set_ylabel('Predictions')
    ax.set_title(f'Prediction vs True Values for {states[i]}_Next')
plt.tight_layout()
plt.show()
