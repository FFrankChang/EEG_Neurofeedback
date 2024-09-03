import pandas as pd
import numpy as np

# 设置随机种子以便结果可复现
np.random.seed(0)

# 创建mock数据的数量
num_entries = 5000  # 可以根据需要调整数据的数量

# 生成观测值数据，范围从1到4
observations = np.random.choice([1, 2, 3, 4], size=num_entries)

# 生成动作数据，只有两种动作：0 (silence), 1 (feedback)
actions = np.random.choice([0, 1], size=num_entries)

# 创建DataFrame
df = pd.DataFrame({
    'Observations': observations,
    'Actions': actions
})

# 文件路径
file_path = r"mock_01.csv"

# 保存到CSV文件
df.to_csv(file_path, index=False)

print(f"Mock data saved to {file_path}")
