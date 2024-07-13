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

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Function to create and save plot for standard deviation
def create_std_plot(data, scenario):
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
    plt.savefig(os.path.join(folder_path, f'steering_angle_std_{scenario}.png'))
    plt.close()

# Function to create and save plot for percentage change
def create_change_plot(data, scenario):
    # Prepare data: Calculate change ratio
    pivot_table = data.pivot_table(index='subject', columns='condition', values='Steering_Angle_Std')
    pivot_table['change_ratio'] = (pivot_table['silence'] - pivot_table['feedback']) / pivot_table['silence']
    
    plt.figure(figsize=(12, 8))
    change_chart = sns.barplot(x=pivot_table.index, y=pivot_table['change_ratio'], color='gray')
    
    # Add data labels
    for p in change_chart.patches:
        change_chart.annotate(format(p.get_height(), '.2f'), 
                              (p.get_x() + p.get_width() / 2., p.get_height()), 
                              ha = 'center', va = 'center', 
                              xytext = (0, 9), 
                              textcoords = 'offset points')
    
    plt.title(f'Change Ratio of Steering Angle Std by Subject ({scenario})')
    plt.xlabel('Subject')
    plt.ylabel('Change Ratio ((Silence - Feedback) / Silence)')
    plt.savefig(os.path.join(folder_path, f'change_ratio_{scenario}.png'))
    plt.close()

# Filter data by scenario and create plots
for scenario in ['easy', 'hard']:
    scenario_data = combined_data[combined_data['scenario'] == scenario]
    create_std_plot(scenario_data, scenario)
    create_change_plot(scenario_data, scenario)
