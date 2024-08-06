import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('grouped_expv1_c01_results.csv')
# Create a new column that combines Subject and Day for the x-axis
df['Subject_Day'] = df['Subject'].astype(str) + '_Day_' + df['Day'].astype(str)

# List of columns to visualize
columns = [
    "Min_TTC",
    "Steering_Angle_STD",
    "Acceleration_x_Mean",
    "Acceleration_x_STD",
    "Acceleration_x_Change_Rate_Mean",
    "Road_Exits",
    "Average_Lanes_Per_Change",
    "Successful_Changes",
    "Total_Successful_Change_Time"
]

# Setting up the color palette
palette = {'feedback': 'lightblue', 'silence': 'grey'}

# Creating a figure to hold all the subplots
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 12))
fig.suptitle('Performance Metrics by Subject-Day and Condition')

# Loop through each metric and plot it in a separate subplot
for i, column in enumerate(columns):
    ax = axes[i//3, i%3]
    sns.barplot(x='Subject_Day', y=column, hue='Condition', data=df, ax=ax, palette=palette, dodge=True)
    ax.set_title(column)
    ax.set_xlabel('Subject-Day')
    ax.set_ylabel('Value')
    ax.legend(title='Condition')

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig('performance_metrics.png')

# Show the plot
plt.show()
