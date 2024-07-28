import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\grouped_expv1_c01_results_e_sham.csv'
data = pd.read_csv(file_path)

# List of metrics to plot
metrics = [
    "Min_TTC", "Steering_Angle_STD", "Acceleration_x_Mean", 
    "Acceleration_x_STD", "Acceleration_x_Change_Rate_Mean", 
    "Road_Exits", "Average_Lanes_Per_Change", 
    "Successful_Changes", "Total_Successful_Change_Time"
]

# Setting up the figure and axes for the boxplots
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(8, 18), constrained_layout=True)
palette = {"silence": "gray", "feedback": "lightcoral"}  # blue color for feedback, gray for silence

# Flatten the axes array for easier indexing
axes = axes.flatten()

# Loop over the metrics and create a boxplot for each
for i, metric in enumerate(metrics):

    sns.boxplot(x='Condition', y=metric, data=data, ax=axes[i],palette=palette)
    axes[i].set_title(metric, fontsize=6)
    axes[i].tick_params(labelsize=6)  
    axes[i].set_ylabel('', fontsize=6)      # Adjust y-axis label font size
      # Adjust tick label font size
  # Adjust title font size
    axes[i].set_title(metric)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')
    axes[i].tick_params(labelrotation=45)
plt.savefig('sham.png')
# Improve layout and show the plot
plt.show()

