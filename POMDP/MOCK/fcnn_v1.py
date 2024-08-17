import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 定义网络结构
class ValueNetwork(nn.Module):
    def __init__(self):
        super(ValueNetwork, self).__init__()
        self.fc1 = nn.Linear(2, 64)  # 两个输入状态
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)  # 一个输出，值函数

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 实例化网络和优化器
value_net = ValueNetwork()
optimizer = optim.Adam(value_net.parameters(), lr=0.01)

# 模拟环境函数
def simulate_environment(state, action):
    next_state = state + np.random.normal(0, 0.1, 2)  # 随机转移
    reward = -((state[0] - 0.5)**2 + state[1])  # 奖励函数
    return next_state, reward

# 训练过程
gamma = 0.9  # 折扣因子
num_episodes = 1000  # 总迭代次数

for episode in range(num_episodes):
    state = np.random.rand(2)  # 初始化状态
    total_loss = 0

    for _ in range(100):  # 每个episode的时间步
        action = np.random.choice([0, 1])  # 随机选择动作
        next_state, reward = simulate_environment(state, action)

        # 转换为张量
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
        reward_tensor = torch.FloatTensor([reward])

        # 预测当前状态和下一个状态的值
        current_value = value_net(state_tensor)
        next_value = value_net(next_state_tensor)
        
        # 计算目标和损失
        target_value = reward_tensor + gamma * next_value
        loss = (current_value - target_value.detach()).pow(2).mean()
        total_loss += loss.item()

        # 梯度下降更新权重
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        state = next_state

    if episode % 100 == 0:
        print(f'Episode {episode}: Loss = {total_loss:.4f}')

# 保存模型
torch.save(value_net.state_dict(), 'value_network.pth')
print("Model saved.")
