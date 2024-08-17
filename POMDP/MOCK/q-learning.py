import numpy as np
import random

# 环境参数
states = range(16)  # 状态空间
actions = ['up', 'down', 'left', 'right']  # 动作空间
gamma = 0.9  # 折扣因子
alpha = 0.1  # 学习率
epsilon = 0.1  # 探索率
episodes = 1000  # 训练轮数

# 转移概率和奖励函数（假设已知）
# 转移概率 P(s'|s,a) 和奖励函数 R(s,a)
def step(state, action):
    row, col = state // 4, state % 4
    if action == 'up':
        next_state = max(0, row - 1) * 4 + col
    elif action == 'down':
        next_state = min(3, row + 1) * 4 + col
    elif action == 'left':
        next_state = row * 4 + max(0, col - 1)
    elif action == 'right':
        next_state = row * 4 + min(3, col + 1)
    
    if next_state == 15:
        return next_state, 1  # 到达终点，奖励1
    else:
        return next_state, 0  # 其他情况奖励为0

# Q值初始化
Q = np.zeros((len(states), len(actions)))

# Q-learning算法
for episode in range(episodes):
    state = random.choice(states)  # 随机初始化状态
    while state != 15:  # 直到到达终点状态
        # ε-greedy选择动作
        if random.uniform(0, 1) < epsilon:
            action_index = random.choice(range(len(actions)))  # 随机选择动作
        else:
            action_index = np.argmax(Q[state])  # 选择Q值最大的动作

        action = actions[action_index]
        next_state, reward = step(state, action)

        # 更新Q值
        Q[state, action_index] = Q[state, action_index] + alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action_index]
        )

        state = next_state  # 转移到下一个状态

# 输出最优策略
optimal_policy = [actions[np.argmax(Q[state])] for state in states]
print("Optimal Policy:")
for i in range(4):
    print(optimal_policy[i * 4:(i + 1) * 4])

# 输出Q值
print("\nQ-values:")
for state in states:
    print(f"State {state}: {Q[state]}")
