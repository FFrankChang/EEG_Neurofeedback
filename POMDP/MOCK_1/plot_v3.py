import matplotlib.pyplot as plt
import networkx as nx
import random

# 创建一个有向图
G = nx.DiGraph()

# 添加节点
states = ['optimal', 'other']
observations = ['O1', 'O2', 'O3', 'O4']
G.add_node('optimal', pos=(0, 1), size=3000, color='lightgray')
G.add_node('other', pos=(4, 1), size=3000, color='lightgray')

# 添加观测节点
pos = { 'optimal': (0, 1), 'other': (4, 1) }
node_sizes = [3000, 3000]
node_colors = ['lightgray', 'lightgray']

for i, obs in enumerate(observations):
    G.add_node(obs, pos=(2, 2-i), size=4000, color='skyblue')
    pos[obs] = (2, 2-i)
    node_sizes.append(4000)
    node_colors.append('skyblue')

def generate_random_weights():
    # 生成四个随机数
    weights = [random.random() for _ in range(4)]
    # 归一化使其和为1
    total = sum(weights)
    normalized_weights = [w / total for w in weights]
    return normalized_weights

# 对 'optimal' 节点设置权重
optimal_weights = generate_random_weights()
G.add_edge('optimal', 'O1', weight=optimal_weights[0])
G.add_edge('optimal', 'O2', weight=optimal_weights[1])
G.add_edge('optimal', 'O3', weight=optimal_weights[2])
G.add_edge('optimal', 'O4', weight=optimal_weights[3])

# 对 'other' 节点设置权重
other_weights = generate_random_weights()
G.add_edge('other', 'O1', weight=other_weights[0])
G.add_edge('other', 'O2', weight=other_weights[1])
G.add_edge('other', 'O3', weight=other_weights[2])
G.add_edge('other', 'O4', weight=other_weights[3])
# 绘制图形
plt.figure(figsize=(10, 6))
nx.draw_networkx(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]:.3f}' for u, v, d in G.edges(data=True)}, font_color='black')

plt.title('Observation Probabilities')
plt.axis('off')  # 关闭坐标轴
plt.show()
