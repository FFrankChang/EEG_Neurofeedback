import pandas as pd
import numpy as np

# 读取观测数据文件
file_path = r"D:\gitee\EEG_Neurofeedback\mock_01.csv"
observations_data = pd.read_csv(file_path)

# 提取观测数据和动作
observations = observations_data['Observations'].values
actions = observations_data['Actions'].values

# 数据验证
assert np.all(np.isin(observations, [1, 2, 3, 4])), "Observations列中的数据不在预期范围内"
assert np.all(np.isin(actions, [0, 1])), "Actions列中的数据不在预期范围内"

# 初始化参数
states = ['optimal', 'other']
num_states = len(states)
num_actions = 2  # 动作数量: 0 (silence), 1 (feedback)

# 初始化状态转移概率矩阵 (state, action, next_state)
transition_probabilities = np.full((num_states, num_actions, num_states), 1 / num_states)

# 初始化观测概率矩阵 (state, observation)
observation_probabilities = np.full((num_states, 4), 0.25)  # Assume uniform initial probabilities

# 初始化先验概率
prior_probabilities = np.full(num_states, 1 / num_states)

# 辅助函数，用于安全除法
def safe_divide(a, b):
    """Helper function to safely divide arrays."""
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.true_divide(a, b)
        result[~np.isfinite(result)] = 0  # Set infinities and NaNs to 0
    return result

# 定义E-step函数
def e_step(prior, trans_probs, obs_probs, obs, actions):
    num_obs = len(obs)
    alpha = np.zeros((num_obs, num_states))
    beta = np.zeros((num_obs, num_states))
    gamma = np.zeros((num_obs, num_states))
    alpha[0, :] = prior * obs_probs[:, obs[0] - 1]  # Adjust for 0-based index
    alpha[0, :] = safe_divide(alpha[0, :], np.sum(alpha[0, :]) + 1e-10)
    for t in range(1, num_obs):
        for j in range(num_states):
            alpha[t, j] = np.sum(alpha[t-1, :] * trans_probs[:, actions[t-1], j]) * obs_probs[j, obs[t] - 1]
        alpha[t, :] = safe_divide(alpha[t, :], np.sum(alpha[t, :]) + 1e-10)
    beta[-1, :] = 1
    for t in range(num_obs - 2, -1, -1):
        for i in range(num_states):
            beta[t, i] = np.sum(beta[t + 1, :] * trans_probs[i, actions[t], :] * obs_probs[:, obs[t + 1] - 1])
        beta[t, :] = safe_divide(beta[t, :], np.sum(beta[t, :]) + 1e-10)
    gamma = alpha * beta
    gamma = safe_divide(gamma, np.sum(gamma, axis=1, keepdims=True) + 1e-10)
    return alpha, beta, gamma

# 定义M-step函数
def m_step(gamma, obs, actions):
    num_states = gamma.shape[1]
    num_obs_values = 4
    new_prior = gamma[0, :]
    new_obs_probs = np.zeros((num_states, num_obs_values))
    for s in range(num_states):
        for o in range(num_obs_values):
            new_obs_probs[s, o] = np.sum(gamma[:, s] * (obs == (o + 1))) / np.sum(gamma[:, s])
    new_trans_probs = np.zeros((num_states, num_actions, num_states))
    for t in range(len(obs) - 1):
        for i in range(num_states):
            for a in range(num_actions):
                for j in range(num_states):
                    new_trans_probs[i, a, j] += gamma[t, i] * (actions[t] == a) * gamma[t + 1, j]
    new_trans_probs = safe_divide(new_trans_probs, np.sum(new_trans_probs, axis=2, keepdims=True) + 1e-10)
    return new_prior, new_obs_probs, new_trans_probs

# EM算法执行
def em_algorithm(prior, trans_probs, obs_probs, obs, actions, num_iterations=10):
    for iteration in range(num_iterations):
        alpha, beta, gamma = e_step(prior, trans_probs, obs_probs, obs, actions)
        prior, obs_probs, trans_probs = m_step(gamma, obs, actions)
        print(f"Iteration {iteration + 1} completed.")
    return prior, obs_probs, trans_probs

# 运行EM算法
final_prior, final_obs_probs, final_trans_probs = em_algorithm(prior_probabilities, transition_probabilities, observation_probabilities, observations, actions)

# 打印最终结果
# 转换状态转移概率矩阵为表格
transition_df = pd.DataFrame([(s, a, ns, final_trans_probs[i, a, j]) 
                              for i, s in enumerate(states) 
                              for a in range(num_actions) 
                              for j, ns in enumerate(states)], 
                             columns=["from_state", "action", "to_state", "probability"])

# 转换观测概率矩阵为表格
observation_df = pd.DataFrame([(s, o + 1, final_obs_probs[i, o]) 
                               for i, s in enumerate(states) 
                               for o in range(4)], 
                              columns=["state", "observation", "probability"])

print("State Transition Probabilities:")
print(transition_df)
print("\nObservation Probabilities:")
print(observation_df)
