import pandas as pd
import matplotlib.pyplot as plt

duration = 60
# Load the data
file_path = rf'D:\gitee\EEG_Neurofeedback\POMDP\results\results_ex\final_results_{duration}s.csv'
data = pd.read_csv(file_path)

# Filter data where Condition is 'feedback'
feedback_data = data[data['Condition'] == 'feedback']

# Group data by 'Day'
grouped = feedback_data.groupby('Day')

# Columns to plot
columns_to_plot = ['Min_TTC', 'Steering_Angle_STD', 'Acceleration_x_Mean', 'Acceleration_x_STD', 'Acceleration_x_Change_Rate_Mean', 'Road_Exits']

# Create a figure with 2 rows and 3 columns for the subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
axes = axes.flatten()  # Flatten the array of axes to make indexing easier

# Plot each column in a subplot
for index, column in enumerate(columns_to_plot):
    data_to_plot = [group[column].tolist() for _, group in grouped]
    # Customizing boxplot styles
    boxprops = dict(linestyle='-', linewidth=1)
    medianprops = dict(linestyle='-', linewidth=1)
    whiskerprops = dict(linestyle='--', linewidth=1)
    capprops = dict(linestyle='-', linewidth=1)
    flierprops = dict(marker='o', markerfacecolor='black', markersize=5, linestyle='none')

    # Assign color for specific group
    box_colors = ['blue' if label == 'D02' else 'black' for label in grouped.groups.keys()]

    # Create the boxplot with adjusted width and specific colors
    bplot = axes[index].boxplot(data_to_plot, labels=grouped.groups.keys(), boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops, flierprops=flierprops, patch_artist=True, widths=0.5)
    
    # Apply colors to the boxplot
    for patch, color in zip(bplot['boxes'], box_colors):
        patch.set_facecolor(color)

    axes[index].set_title(f'{column}')
    axes[index].set_xlabel('Trails')
    axes[index].set_ylabel(column)
    axes[index].grid(True)  # Add grid for better readability
fig.suptitle(f"Metrics_{duration}s")
# Tight layout to prevent overlap
plt.tight_layout()

# Save the figure
plt.savefig(f'boxplots_{duration}s.png')

# Show the plot
# plt.show()
