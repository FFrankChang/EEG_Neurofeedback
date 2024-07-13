import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import os

# Specify the folder containing the CSV files
folder_path = r'data_analysis/results/20240703'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Combine all CSV data into one DataFrame
combined_data = pd.concat((pd.read_csv(file) for file in csv_files))

# Filter data by scenario
easy_data = combined_data[combined_data['scenario'] == 'easy']
hard_data = combined_data[combined_data['scenario'] == 'hard']

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Function to create and save plot
def create_plot(data, scenario):
    plt.figure(figsize=(12, 8))
    palette_colors = {"silence": "gray", "feedback": "lightblue"}
    bar_chart = sns.barplot(x='subject', y='Steering_Angle_Std', hue='condition', data=data,palette=palette_colors,ci=None)
    
    # Add data labels
    for p in bar_chart.patches:
        bar_chart.annotate(format(p.get_height(), '.3f'), 
                           (p.get_x() + p.get_width() / 2., p.get_height()), 
                           ha = 'center', va = 'center', 
                           xytext = (0, 9), 
                           textcoords = 'offset points')
    
    plt.title(f'Standard Deviation of Steering Angle by Subject and Condition ({scenario})')
    plt.xlabel('Subject')
    plt.ylabel('Standard Deviation of Steering Angle')
    
    # Save the plot
    plt.savefig(os.path.join(folder_path, f'steering_angle_std_{scenario}.png'))
    plt.close()

# Create and save plots for both scenarios
create_plot(easy_data, 'easy')
create_plot(hard_data, 'hard')
