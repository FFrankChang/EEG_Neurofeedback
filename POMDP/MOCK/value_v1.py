import numpy as np

def value_iteration(states, actions, transition_prob, reward, gamma=0.9, theta=1e-6):
    V = {s: 0 for s in states}
    
    while True:
        delta = 0
        
        for s in states:
            v = V[s]
            V[s] = max(
                sum(
                    transition_prob.get((s, a, s_prime), 0) * 
                    (reward.get((s, a, s_prime), 0) + gamma * V[s_prime])
                    for s_prime in states
                ) for a in actions
            )
            delta = max(delta, abs(v - V[s]))
        
        if delta < theta:
            break
    
    policy = {}
    for s in states:
        policy[s] = max(actions, key=lambda a: sum(
            transition_prob.get((s, a, s_prime), 0) *
            (reward.get((s, a, s_prime), 0) + gamma * V[s_prime])
            for s_prime in states
        ))
    
    return V, policy


# Example usage
states = ['s1', 's2', 's3']
actions = ['a1', 'a2']
transition_prob = {
    ('s1', 'a1', 's1'): 0.5, ('s1', 'a1', 's2'): 0.5, ('s1', 'a2', 's1'): 0.7, ('s1', 'a2', 's3'): 0.3,
    ('s2', 'a1', 's1'): 0.6, ('s2', 'a1', 's3'): 0.4, ('s2', 'a2', 's2'): 0.9, ('s2', 'a2', 's3'): 0.1,
    ('s3', 'a1', 's1'): 0.3, ('s3', 'a1', 's2'): 0.7, ('s3', 'a2', 's3'): 1.0,
}
reward = {
    ('s1', 'a1', 's1'): 5, ('s1', 'a1', 's2'): 10, ('s1', 'a2', 's1'): 1, ('s1', 'a2', 's3'): 7,
    ('s2', 'a1', 's1'): 2, ('s2', 'a1', 's3'): 4, ('s2', 'a2', 's2'): 8, ('s2', 'a2', 's3'): 12,
    ('s3', 'a1', 's1'): 3, ('s3', 'a1', 's2'): 6, ('s3', 'a2', 's3'): 9,
}

V, policy = value_iteration(states, actions, transition_prob, reward)

print("Optimal Value Function:")
for state, value in V.items():
    print(f"V({state}) = {value:.2f}")

print("\nOptimal Policy:")
for state, action in policy.items():
    print(f"Policy({state}) = {action}")
