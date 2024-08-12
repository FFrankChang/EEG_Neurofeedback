import pandas as pd
import numpy as np

# 读取观测数据文件
file_path = r"C:\Users\Lenovo\EEG_Neurofeedback\POMDP\combined_observation_sequences.csv"
observations_data = pd.read_csv(file_path)

# 提取RELIANCE列作为观测数据
reliance_observations = observations_data['RELIANCE'].values

# 提取DRIVING_STYLE和VISIBILITY列作为动作数据
driving_style = observations_data['DRIVING_STYLE'].values
visibility = observations_data['VISIBILITY'].values

# 数据验证
assert np.all(np.isin(reliance_observations, [0, 1])), "RELIANCE列中的数据不在预期范围内"
assert np.all(np.isin(driving_style, [1, 2, 3, 4])), "DRIVING_STYLE列中的数据不在预期范围内"
assert np.all(np.isin(visibility, [0, 1])), "VISIBILITY列中的数据不在预期范围内"

# 初始化参数
states = ['high', 'low']  # 仅考虑 trust 状态
num_states = len(states)

# 定义动作的组合
driving_styles = [1, 2, 3, 4]
visibilities = [0, 1]
actions = [(ds, v) for ds in driving_styles for v in visibilities]
num_actions = len(actions)

# 初始化状态转移概率矩阵 (state, action, next_state)
transition_probabilities = np.full((num_states, num_actions, num_states), 1 / num_states)

# 初始化观测概率矩阵 (state, observation)
observation_probabilities = np.array([
    [0.8, 0.2],  # high trust (no_takeover, takeover)
    [0.3, 0.7]   # low trust (no_takeover, takeover)
])

# 初始化先验概率
prior_probabilities = np.full(num_states, 1 / num_states)

def safe_divide(a, b):
    """Helper function to safely divide arrays."""
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.true_divide(a, b)
        result[~np.isfinite(result)] = 0  # 设置无穷和NaN值为0
    return result

def e_step(prior, trans_probs, obs_probs, obs, actions):
    num_obs = len(obs)
    
    # 前向后向算法计算后验概率
    alpha = np.zeros((num_obs, num_states))
    beta = np.zeros((num_obs, num_states))
    gamma = np.zeros((num_obs, num_states))

    # 前向步骤
    alpha[0, :] = prior * obs_probs[:, obs[0]]
    alpha[0, :] = safe_divide(alpha[0, :], np.sum(alpha[0, :]) + 1e-10)
    
    for t in range(1, num_obs):
        for j in range(num_states):
            alpha[t, j] = np.sum(alpha[t-1, :] * trans_probs[:, actions[t-1], j]) * obs_probs[j, obs[t]]
        alpha[t, :] = safe_divide(alpha[t, :], np.sum(alpha[t, :]) + 1e-10)

    # 后向步骤
    beta[-1, :] = 1
    for t in range(num_obs - 2, -1, -1):
        for i in range(num_states):
            beta[t, i] = np.sum(beta[t + 1, :] * trans_probs[i, actions[t], :] * obs_probs[:, obs[t + 1]])
        beta[t, :] = safe_divide(beta[t, :], np.sum(beta[t, :]) + 1e-10)
    
    # 计算gamma
    gamma = alpha * beta
    gamma = safe_divide(gamma, np.sum(gamma, axis=1, keepdims=True) + 1e-10)
    
    return alpha, beta, gamma

def m_step(gamma, obs, actions):
    num_states = gamma.shape[1]
    
    # 更新先验概率
    new_prior = gamma[0, :]
    
    # 更新观测概率
    new_obs_probs = np.zeros((num_states, 2))
    for s in range(num_states):
        if np.sum(gamma[:, s]) == 0:
            continue
        for o in range(2):  # 两种观测值：0 和 1
            new_obs_probs[s, o] = np.sum(gamma[:, s] * (obs == o)) / np.sum(gamma[:, s])
    
    # 更新状态转移概率
    new_trans_probs = np.zeros((num_states, num_actions, num_states))
    for t in range(len(obs) - 1):
        for i in range(num_states):
            if np.sum(gamma[t, i]) == 0:
                continue
            for a in range(num_actions):
                for j in range(num_states):
                    new_trans_probs[i, a, j] += gamma[t, i] * (actions[t] == a) * gamma[t + 1, j]
    new_trans_probs = safe_divide(new_trans_probs, np.sum(new_trans_probs, axis=2, keepdims=True) + 1e-10)
    
    return new_prior, new_obs_probs, new_trans_probs

def em_algorithm(prior, trans_probs, obs_probs, obs, actions, num_iterations=200):
    for iteration in range(num_iterations):
        alpha, beta, gamma = e_step(prior, trans_probs, obs_probs, obs, actions)
        prior, obs_probs, trans_probs = m_step(gamma, obs, actions)
        print(f"Iteration {iteration + 1}")
        
    return prior, obs_probs, trans_probs

# 将driving_style和visibility数据转换为索引组合动作
action_indices = np.array([actions.index((ds, v)) for ds, v in zip(driving_style, visibility)])

# 运行EM算法
final_prior, final_obs_probs, final_trans_probs = em_algorithm(prior_probabilities, transition_probabilities, observation_probabilities, reliance_observations, action_indices)

print("最终先验概率:", final_prior)

# 转换状态转移概率矩阵为表格
transitions = []
for i, from_state in enumerate(states):
    for j, to_state in enumerate(states):
        for k, action in enumerate(actions):
            prob = final_trans_probs[i, k, j]
            transitions.append([from_state, to_state, action, prob])

transition_df = pd.DataFrame(transitions, columns=["from", "to", "action", "prob"])

# 转换观测概率矩阵为表格
observations = []
for i, state in enumerate(states):
    for o in range(2):  # 两种观测值：0 和 1
        prob = final_obs_probs[i, o]
        observations.append([state, o, prob])

observation_df = pd.DataFrame(observations, columns=["state", "observation", "prob"])

# 显示状态转移概率表格
print("State Transition Probabilities:")
print(transition_df)

# 显示观测概率表格
print("Observation Probabilities:")
print(observation_df)
