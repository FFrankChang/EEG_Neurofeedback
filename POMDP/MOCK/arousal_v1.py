import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 设置随机种子
np.random.seed(42)

# 生成 arousal 数据
n_samples = 1000
arousal = np.random.uniform(0, 1, n_samples)

# 生成心率和瞳孔大小数据
# 假设基础心率为 60，瞳孔大小为 3mm，随 arousal 线性增加
base_hr = 60
base_ps = 3
hr = base_hr + 40 * arousal + np.random.normal(0, 5, n_samples)  # 心率，随 arousal 线性增加，加入正态噪声
ps = base_ps + 2 * arousal + np.random.normal(0, 0.5, n_samples)  # 瞳孔大小，随 arousal 线性增加，加入正态噪声

# 绘图查看生成的数据分布
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(arousal, hr, alpha=0.6)
plt.xlabel('Arousal')
plt.ylabel('Heart Rate')
plt.title('Heart Rate vs Arousal')

plt.subplot(1, 2, 2)
plt.scatter(arousal, ps, alpha=0.6)
plt.xlabel('Arousal')
plt.ylabel('Pupil Size')
plt.title('Pupil Size vs Arousal')
plt.tight_layout()
plt.show()


# 心率模型
model_hr = LinearRegression()
model_hr.fit(arousal.reshape(-1, 1), hr)

# 瞳孔大小模型
model_ps = LinearRegression()
model_ps.fit(arousal.reshape(-1, 1), ps)

# 输出模型参数
print("Heart Rate model coefficients:", model_hr.coef_, "Intercept:", model_hr.intercept_)
print("Pupil Size model coefficients:", model_ps.coef_, "Intercept:", model_ps.intercept_)
