import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes with positions
positions = {
    'High-(1,0)': (1, 2), 'Low-(1,0)': (1, 1),
    'High-(1,1)': (2, 2), 'Low-(1,1)': (2, 1),
    'High-(2,0)': (3, 2), 'Low-(2,0)': (3, 1),
    # Add more nodes here based on the structure you need
}

# Add edges along with the weights (probabilities)
edges = [
    ('High-(1,0)', 'High-(1,1)', 0.924),
    ('High-(1,0)', 'Low-(1,1)', 0.076),
    ('Low-(1,0)', 'High-(1,1)', 0.277),
    ('Low-(1,0)', 'Low-(1,1)', 0.723),
    # Add more edges here according to your specific transitions
]

# Adding nodes and edges to the graph
for node, pos in positions.items():
    G.add_node(node, pos=pos)
for u, v, w in edges:
    G.add_edge(u, v, weight=w)

# Draw the graph
plt.figure(figsize=(10, 5))
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', node_size=3000, edge_color='k', font_size=9, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, positions, edge_labels=labels)

plt.title('State Transition Diagram')
plt.show()
