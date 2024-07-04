import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
# 模拟数据生成
np.random.seed(42)
# 生成两个类别的数据，每个类别100个样本，每个样本64个通道，100个时间点
data_class_1 = np.random.randn(100, 64, 100) + 2  # 第一类中心在2
data_class_2 = np.random.randn(100, 64, 100) - 2  # 第二类中心在-2

# 计算协方差矩阵和特征值分解
def compute_projection_matrix(data):
    covariance_matrix = np.cov(data.reshape(data.shape[0], -1).T)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    # 选择最大的6个特征向量
    projection_matrix = eigenvectors[:, -6:]
    return projection_matrix

proj_matrix_1 = compute_projection_matrix(data_class_1)
proj_matrix_2 = compute_projection_matrix(data_class_2)

# 特征空间构建
def project_data(data, proj_matrix):
    flat_data = data.reshape(data.shape[0], -1)
    return flat_data @ proj_matrix

features_1 = project_data(data_class_1, proj_matrix_1)
features_2 = project_data(data_class_2, proj_matrix_2)

# LDA模型训练
lda = LDA()
X = np.vstack((features_1, features_2))
y = np.array([1]*100 + [2]*100)
lda.fit(X, y)

# 实时反馈模拟
def real_time_feedback(new_data, proj_matrix, lda, window_size=5):
    features = project_data(new_data, proj_matrix)
    lda_scores = lda.decision_function(features)
    # 实现5秒滑动窗口平均
    moving_average = np.convolve(lda_scores, np.ones(window_size)/window_size, mode='valid')
    return moving_average

# 模拟新数据
new_data = np.random.randn(20, 64, 100)
moving_average_output = real_time_feedback(new_data, proj_matrix_1, lda)

# 结果可视化
plt.plot(moving_average_output)
plt.title("Real-time Feedback Signal")
plt.xlabel("Time")
plt.ylabel("LDA Output")
plt.show()
