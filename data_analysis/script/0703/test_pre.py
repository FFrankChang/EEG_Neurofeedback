import pandas as pd
import os

def calculate_averages(input_file):
    # Load the CSV file
    data = pd.read_csv(input_file)
    subject_id = data['subject'].iloc[0]

    # Group the data by 'scenario' and 'condition', then calculate the average of 'Steering_Angle_Std'
    grouped_data = data.groupby(['scenario', 'condition'])['Steering_Angle_Std'].mean().reset_index()
    
    # Add a column for the subject based on the file name
    grouped_data['subject'] = subject_id
    grouped_data = grouped_data[['subject', 'scenario', 'condition', 'Steering_Angle_Std']]

    return grouped_data

def process_all_files(directory, output_file):
    results_list = []
    
    # List all csv files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            results_list.append(calculate_averages(file_path))
    
    # Concatenate all results into a single dataframe
    all_results = pd.concat(results_list, ignore_index=True)
    
    # Save the final dataframe to a CSV file
    all_results.to_csv(output_file, index=False)
    
    return all_results

# Define directory path and output file path
directory_path =  r'data_analysis/results/20240703'
output_path =  r'data_analysis/results/20240703/all.csv'

# Process all CSV files in the specified directory
final_results = process_all_files(directory_path, output_path)

# Display the final results
print(final_results)
