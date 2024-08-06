import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('grouped_expv1_c01_results_d.csv')

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
palette = {'feedback': 'lightblue', 'silence': 'lightcoral'}

# Calculate number of unique Subject_Day combinations
unique_subject_days = len(df['Subject_Day'].unique())

# Loop through each metric and create a separate plot
for column in columns:
    plt.figure(figsize=(12, 8))  # Setting the figure size
    ax = sns.barplot(x='Subject_Day', y=column, hue='Condition', data=df, palette=palette, dodge=True)
    plt.title(f'Performance Metric: {column}')
    plt.xlabel('Subject-Day')
    plt.ylabel('Value')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)  # Rotate x-axis labels to vertical
    
    # Adding alternate background colors for each subject
    for i in range(0, unique_subject_days, 2):  # Adjust to cover two entries per subject
        color = 'grey' if (i // 2) % 2 == 0 else 'lightgrey'
        ax.axvspan(i-0.5, i+1.5, color=color, alpha=0.3, zorder=0)

    plt.legend(title='Condition')
    plt.tight_layout()  # Adjust layout

    # Save each figure with a unique name based on the metric
    plt.savefig(f'C01_{column}_performance.png')
    plt.close()  # Close the current figure to avoid memory issues
