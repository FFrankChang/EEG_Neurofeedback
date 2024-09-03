import numpy as np

def initialize_probabilities(states, actions, observations):
    # 初始化状态转移概率 T(s, a, s') 和观测概率 Z(s, o)
    T = np.random.rand(len(states), len(actions), len(states))
    for i in range(len(states)):
        for j in range(len(actions)):
            T[i, j] /= T[i, j].sum()

    Z = np.random.rand(len(states), len(observations))
    for i in range(len(states)):
        Z[i] /= Z[i].sum()

    return T, Z

def normalize_probabilities(probs):
    # 归一化概率并修复小数点精度问题
    normalized_probs = probs / np.sum(probs)
    if np.sum(normalized_probs) != 1.0:
        normalized_probs[-1] += 1.0 - np.sum(normalized_probs)
    return normalized_probs

def simulate_step(state, action, T, Z, states, R, observations):
    # 模拟从给定状态和动作转移到下一个状态
    normalized_probs = normalize_probabilities(T[state, action])
    next_state = np.random.choice(range(len(states)), p=normalized_probs)
    # 正确使用观测的数量来选择观测
    observation = np.random.choice(range(len(observations)), p=normalize_probabilities(Z[next_state]))
    next_state_from_obs = observation_to_state(observation, Z)
    reward = R[states[state]][actions[action]]
    return next_state_from_obs, reward


def observation_to_state(observation, Z):
    # 简单的观测到状态的映射函数
    return np.argmax(Z[:, observation])

def update_Q(Q, state, action, reward, next_state, alpha, gamma):
    # Q-learning 更新公式
    best_future_q = np.max(Q[next_state])
    Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * best_future_q)

def train(Q, T, Z, states, actions, R, observations, episodes, steps_per_episode, alpha, gamma):
    # 训练 Q-learning 算法
    for episode in range(episodes):
        state = np.random.randint(len(states))  # 随机初始状态
        for step in range(steps_per_episode):
            action = np.random.randint(len(actions))  # 随机选择动作
            next_state, reward = simulate_step(state, action, T, Z, states, R, observations)
            update_Q(Q, state, action, reward, next_state, alpha, gamma)
            state = next_state

# 假设设置
states = ['optimal', 'other']  # 信念状态
actions = ['a0', 'a1']
observations = ['obs1', 'obs2', 'obs3', 'obs4']

# 奖励函数示例，使用字典
R = {
    'optimal': {'a0': 0, 'a1': -1},
    'other': {'a0': -1, 'a1': 2}
}

# 初始化概率
T, Z = initialize_probabilities(states, actions, observations)

# Q-table 初始化
Q = np.zeros((len(states), len(actions)))

# 训练参数
gamma = 0.9  # 折扣因子
alpha = 0.1  # 学习率
episodes = 1000
steps_per_episode = 10

# 开始训练
train(Q, T, Z, states, actions, R, observations, episodes, steps_per_episode, alpha, gamma)

# 输出最终的 Q-table
print("Q-table:")
print(Q)
