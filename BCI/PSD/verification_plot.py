import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV
data_file_path = '11111.csv'  # Update this path with your actual file path
data = pd.read_csv(data_file_path)

# Plotting each band mean
plt.figure(figsize=(12, 10))

# Alpha band plot
plt.subplot(4, 1, 1)
plt.plot(data['alpha_mean'], label='Alpha Mean')
plt.title('Alpha Band Mean')
plt.xlabel('Time Point')
plt.ylabel('Mean Value')
plt.legend()

# Beta band plot
plt.subplot(4, 1, 2)
plt.plot(data['beta_mean'], label='Beta Mean')
plt.title('Beta Band Mean')
plt.xlabel('Time Point')
plt.ylabel('Mean Value')
plt.legend()

# Theta band plot
plt.subplot(4, 1, 3)
plt.plot(data['theta_mean'], label='Theta Mean')
plt.title('Theta Band Mean')
plt.xlabel('Time Point')
plt.ylabel('Mean Value')
plt.legend()

# Delta band plot
plt.subplot(4, 1, 4)
plt.plot(data['delta_mean'], label='Delta Mean')
plt.title('Delta Band Mean')
plt.xlabel('Time Point')
plt.ylabel('Mean Value')
plt.legend()

# Improve layout and show the plot
plt.tight_layout()
plt.show()
