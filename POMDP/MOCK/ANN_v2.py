import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 设置随机种子以复现结果
np.random.seed(42)

# 生成模拟数据
n_samples = 1000
arousal = np.random.uniform(0, 1, n_samples)
workload = np.random.uniform(0, 1, n_samples)
action = np.random.choice([0, 1], n_samples)  # 0 for Silence, 1 for Feedback

# 定义行动的效应大小
effect_a = 0.1  # Arousal 增加的基本量
effect_w = -0.05  # Workload 减少的基本量

# 生成下一个时间点的状态
arousal_next = arousal + effect_a * action + np.random.normal(0, 0.1, n_samples)
workload_next = workload + effect_w * action + np.random.normal(0, 0.1, n_samples)

# 组装成 DataFrame
data = pd.DataFrame({
    'Arousal': arousal,
    'Workload': workload,
    'Action': action,
    'Arousal_Next': arousal_next,
    'Workload_Next': workload_next
})
# 划分训练集和测试集
features = data[['Arousal', 'Workload', 'Action']]
targets = data[['Arousal_Next', 'Workload_Next']]
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# 构建神经网络模型
model = MLPRegressor(hidden_layer_sizes=(10, 10), activation='relu', max_iter=500, random_state=42, verbose=True, tol=1e-4)
model.fit(X_train, y_train)

# 收集每个epoch的损失
training_loss = model.loss_curve_
# 绘制损失函数变化图
plt.figure(figsize=(10, 6))
plt.plot(training_loss, marker='o', linestyle='-', color='blue',alpha =0.5)
plt.title('Training Loss Over Iterations')
plt.xlabel('Epochs')
plt.ylabel('Loss (MSE)')
plt.grid(True)
plt.show()
