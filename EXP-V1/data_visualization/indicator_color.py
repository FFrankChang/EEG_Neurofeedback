import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the uploaded CSV file
file_path = 'xx.csv'
data = pd.read_csv(file_path)

# Set up the plot
plt.figure(figsize=(12, 10))

# Transpose the data so that rows become columns and columns become rows
data_transposed = data.set_index(['Subject', 'Day']).T

# Create a color map for values
cmap = sns.light_palette("lightgreen", as_cmap=True)

# Plot the heatmap
sns.heatmap(data_transposed, cmap=cmap, annot=True, cbar=False, fmt='d', linewidths=.5, linecolor='black')

# Set plot title and labels
plt.title('Heatmap of Data (1s highlighted)')
plt.xlabel('Entries')
plt.ylabel('Metrics')

# Display the plot
plt.show()
