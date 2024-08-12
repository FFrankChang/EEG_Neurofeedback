import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 定义初始状态概率
initial_state_prob = {
    'workload': {'high': 0.4176, 'low': 0.5833},
    'trust': {'high': 0.75, 'low': 0.25}
}

# 定义状态转移概率
P_workload = {
    'high': {
        (1, 0): {'high': 5.040832e-01, 'low': 4.959168e-01},
        (1, 1): {'high': 4.949514e-01, 'low': 5.050486e-01},
        (2, 0): {'high': 8.037117e-01, 'low': 1.962883e-01},
        (2, 1): {'high': 6.196440e-01, 'low': 3.803560e-01},
        (3, 0): {'high': 4.417525e-01, 'low': 5.582475e-01},
        (3, 1): {'high': 3.067683e-01, 'low': 6.932317e-01},
        (4, 0): {'high': 1.000000e+00, 'low': 3.398811e-286},
        (4, 1): {'high': 9.304026e-01, 'low': 6.959737e-02}
    },
    'low': {
        (1, 0): {'high': 3.004339e-01, 'low': 6.995661e-01},
        (1, 1): {'high': 3.760842e-01, 'low': 6.239158e-01},
        (2, 0): {'high': 5.952219e-01, 'low': 4.047781e-01},
        (2, 1): {'high': 3.263871e-01, 'low': 6.736129e-01},
        (3, 0): {'high': 4.976243e-01, 'low': 5.023757e-01},
        (3, 1): {'high': 4.309326e-01, 'low': 5.690674e-01},
        (4, 0): {'high': 1.000000e+00, 'low': 3.443350e-286},
        (4, 1): {'high': 8.989839e-01, 'low': 1.010161e-01}
    }
}

P_trust = {
    'high': {
        (1, 0): {'high': 9.244790e-01, 'low': 7.552098e-02},
        (1, 1): {'high': 9.999998e-01, 'low': 2.125315e-07},
        (2, 0): {'high': 4.988189e-01, 'low': 5.011811e-01},
        (2, 1): {'high': 5.411758e-01, 'low': 4.588242e-01},
        (3, 0): {'high': 9.314689e-01, 'low': 6.853112e-02},
        (3, 1): {'high': 8.331483e-01, 'low': 1.668516e-01},
        (4, 0): {'high': 5.210995e-30, 'low': 1.000000e+00},
        (4, 1): {'high': 9.396121e-02, 'low': 9.060388e-01}
    },
    'low': {
        (1, 0): {'high': 7.232197e-01, 'low': 2.767803e-01},
        (1, 1): {'high': 5.003193e-01, 'low': 4.996807e-01},
        (2, 0): {'high': 4.970811e-01, 'low': 5.029189e-01},
        (2, 1): {'high': 3.988878e-01, 'low': 6.011122e-01},
        (3, 0): {'high': 6.654830e-01, 'low': 3.345170e-01},
        (3, 1): {'high': 9.999998e-01, 'low': 2.267644e-07},
        (4, 0): {'high': 9.850382e-02, 'low': 9.014962e-01},
        (4, 1): {'high': 2.110443e-01, 'low': 7.889557e-01}
    }
}

# 定义观测概率
O_workload = {
    'high': {1: 3.955233e-08, 2: 9.849474e-01, 3: 1.452473e-08, 4: 1.505254e-02},
    'low': {1: 2.746644e-02, 2: 1.120688e-02, 3: 9.613267e-01, 4: 1.862323e-30}
}

O_trust = {
    'high': {0: 1.000000e+00, 1: 5.908375e-29},
    'low': {0: 1.859575e-03, 1: 9.981404e-01}
}

# 定义奖励函数
rewards = {
    ('high', 'high'): 1,
    ('high', 'low'): -1,
    ('low', 'low'): 0,
    ('low', 'high'): 2,
}

# 定义折扣系数
discount_factor = 0.9

# 定义Q表
def initialize_q_table(states, actions):
    Q = {}
    for state in states:
        Q[state] = {}
        for action in actions:
            Q[state][action] = 0.0
    return Q

# 定义Q-Learning参数
alpha = 0.01  # 学习率
gamma = discount_factor  # 折扣系数
epsilon = 0.25  # 探索率

# 定义状态转移函数
def get_next_state(state, action, P_workload, P_trust):
    trust,workload  = state
    driving_style, visibility = action

    next_workload = 'high' if random.random() < P_workload[workload][action]['high'] else 'low'
    next_trust = 'high' if random.random() < P_trust[trust][action]['high'] else 'low'

    return (next_workload, next_trust)

# Q-Learning训练函数
def q_learning(P_workload, P_trust, rewards, alpha, gamma, epsilon, num_episodes, fixed_visibility):
    states = [('high', 'high'), ('high', 'low'), ('low', 'low'), ('low', 'high')]
    actions = [(1, fixed_visibility), (2, fixed_visibility), (3, fixed_visibility), (4, fixed_visibility)]
    Q = initialize_q_table(states, actions)

    for episode in range(num_episodes):
        # 初始化状态
        state = random.choice(states)

        for step in range(100):
            # 选择动作
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                action = max(Q[state], key=Q[state].get)

            # 获取下一个状态
            next_state = get_next_state(state, action, P_workload, P_trust)

            # 计算奖励
            reward = rewards[next_state]

            # 更新Q值
            best_next_action = max(Q[next_state], key=Q[next_state].get)
            Q[state][action] += alpha * (reward + gamma * Q[next_state][best_next_action] - Q[state][action])

            # 更新状态
            state = next_state

    return Q

# 分别在 visibility = 1 和 visibility = 0 的情况下训练Q-Learning模型
num_episodes = 1000
Q_visibility_1 = q_learning(P_workload, P_trust, rewards, alpha, gamma, epsilon, num_episodes, fixed_visibility=1)
Q_visibility_0 = q_learning(P_workload, P_trust, rewards, alpha, gamma, epsilon, num_episodes, fixed_visibility=0)

# 输出最佳策略
def print_optimal_policy(Q, visibility):
    optimal_policy = {}
    for state in Q:
        optimal_policy[state] = max(Q[state], key=Q[state].get)
    
    print(f"最佳策略 (visibility = {visibility}):")
    for state in optimal_policy:
        workload, trust = state
        action = optimal_policy[state]
        print(f"状态 (工作负荷: {workload}, 信任度: {trust}): 动作 (驾驶风格: {action[0]}, 可见度: {action[1]})")

print_optimal_policy(Q_visibility_1, 1)
print_optimal_policy(Q_visibility_0, 0)

# 可视化Q表
def visualize_q_tables(Q1, Q2, title1, title2):
    q_table1 = []
    q_table2 = []

    for state in Q1:
        for action in Q1[state]:
            q_table1.append([str(state), str(action), Q1[state][action]])

    for state in Q2:
        for action in Q2[state]:
            q_table2.append([str(state), str(action), Q2[state][action]])

    q_df1 = pd.DataFrame(q_table1, columns=['State(T,W)', 'Action', 'Q Value'])
    q_df2 = pd.DataFrame(q_table2, columns=['State(T,W)', 'Action', 'Q Value'])

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    sns.set(style="whitegrid")

    # 绘制热力图1
    pivot_table1 = q_df2.pivot(index='State(T,W)', columns='Action', values='Q Value')
    sns.heatmap(pivot_table1, annot=True, cmap="YlGnBu", fmt=".2f", ax=axes[0])
    axes[1].set_title(title1)

    # 绘制热力图2
    pivot_table2 = q_df1.pivot(index='State(T,W)', columns='Action', values='Q Value')
    sns.heatmap(pivot_table2, annot=True, cmap="YlGnBu", fmt=".2f", ax=axes[1])
    axes[0].set_title(title2)

    plt.show()

visualize_q_tables(Q_visibility_1, Q_visibility_0, "Q-Table Heatmap with Visibility = 1", "Q-Table Heatmap with Visibility = 0")
