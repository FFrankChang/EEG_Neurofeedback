import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import os

# Specify the folder containing the CSV files
folder_path = r'data_analysis/results/20240703'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Loop through each CSV file
for file_path in csv_files:
    # Load the data from CSV
    data = pd.read_csv(file_path)
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='scenario', y='Steering_Angle_Std', hue='condition', data=data)
    
    # Add labels and title
    plt.title('Standard Deviation of Steering Angle by Scenario and Condition')
    plt.xlabel('Scenario')
    plt.ylabel('Standard Deviation of Steering Angle')
    
    # Save the plot as an image file
    # Extract the filename without the extension to use as the image name
    image_name = os.path.basename(file_path).split('.')[0] + '.png'
    plt.savefig(os.path.join(folder_path, image_name))
    
    # Close the plot figure to free up memory
    plt.close()
