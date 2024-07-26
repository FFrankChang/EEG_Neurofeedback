import matplotlib.pyplot as plt
import numpy as np

# Seed for reproducibility
np.random.seed(0)

# Generating synthetic data
# We assume a normal distribution around the mean with some noise
# The mean collision rates are given in percentages, but data needs to be between 0 and 1
means = [0.5, 0.30, 0.12]
std_devs = [0.28, 0.15, 0.1]  # arbitrary standard deviations to generate data
data = [np.clip(np.random.normal(mean, std, 10), 0, 1) for mean, std in zip(means, std_devs)]

# Create a boxplot
fig, ax = plt.subplots()
ax.boxplot(data, showmeans=True)

# Setting the x-axis labels to D1, D2, D3
ax.set_xticklabels(['D1', 'D2', 'D3'])
ax.set_title('Collision Rates Over Three Days of Training')
ax.set_ylabel('Collision Rate')
ax.set_xlabel('Day')

# Show the plot
plt.show()
