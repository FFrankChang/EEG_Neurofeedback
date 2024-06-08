import pandas as pd
import glob
import os

def calculate_average_steering_angle_std(csv_path, output_dir):
    # Load the CSV file
    data = pd.read_csv(csv_path)
    
    # Group the data by 'subject', 'experiment_no', 'scenario', 'condition'
    # and calculate the mean of 'Steering_Angle_Std' for each group
    grouped_data = data.groupby(['subject', 'experiment_no', 'scenario', 'condition'])['Steering_Angle_Std'].mean().reset_index()
    
    # Create a new filename based on the original filename with 'results' appended before the file extension
    base_filename = os.path.basename(csv_path)
    new_filename = os.path.splitext(base_filename)[0] + '_test.csv'
    output_path = os.path.join(output_dir, new_filename)
    
    # Save the grouped data to a new CSV file
    grouped_data.to_csv(output_path, index=False)

# Specify the directory containing the input CSV files and the output directory
input_dir = r'E:\EEG_Neurofeedback\data_analysis\results\20240606\+3sresults'  # Change this to your actual directory path
output_dir = r'E:\EEG_Neurofeedback\data_analysis\results\20240606\+3sresults\all'  # Change this to your desired output directory path

# Get all CSV files in the directory
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

# Process each file
for file_path in csv_files:
    calculate_average_steering_angle_std(file_path, output_dir)
