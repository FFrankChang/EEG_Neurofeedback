import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 假设transition_df和observation_df已经按照之前的代码生成

# Example data for demonstration purposes
# You should replace these with transition_df and observation_df from your actual code output
transition_df = pd.DataFrame({
    'from_state': ['optimal', 'optimal', 'other', 'other'],
    'action': [0, 1, 0, 1],
    'to_state': ['optimal', 'other', 'optimal', 'other'],
    'probability': [0.7, 0.3, 0.4, 0.6]
})

observation_df = pd.DataFrame({
    'state': ['optimal', 'optimal', 'optimal', 'optimal', 'other', 'other', 'other', 'other'],
    'observation': [1, 2, 3, 4, 1, 2, 3, 4],
    'probability': [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
})

# Convert transition probabilities to a pivot table for heatmap
transition_pivot = transition_df.pivot_table(index=['from_state', 'action'], columns='to_state', values='probability', fill_value=0)

# Convert observation probabilities to a pivot table for heatmap
observation_pivot = observation_df.pivot_table(index='state', columns='observation', values='probability', fill_value=0)

# Plotting transition probabilities heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(transition_pivot, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('State Transition Probabilities')
plt.ylabel('From State, Action')
plt.xlabel('To State')
plt.show()

# Plotting observation probabilities heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(observation_pivot, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Observation Probabilities')
plt.ylabel('State')
plt.xlabel('Observation')
plt.show()
