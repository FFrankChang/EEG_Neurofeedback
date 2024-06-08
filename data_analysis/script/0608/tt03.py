import pandas as pd

def process_and_save_data(input_csv_path, output_csv_path):
    # Load the CSV file
    data = pd.read_csv(input_csv_path)
    
    # Filter data for 'hard' scenario
    hard_data = data[data['scenario'] == 'easy']
    
    # Group by 'subject' and 'condition', and calculate the mean of 'Steering_Angle_Std'
    grouped_data = hard_data.groupby(['subject', 'condition'])['Steering_Angle_Std'].mean().reset_index()
    
    # Save the results to a new CSV file
    grouped_data.to_csv(output_csv_path, index=False)

# Specify the path to the input and output CSV files
input_path = r'E:\EEG_Neurofeedback\+3s_result.csv'  # Replace with your actual input file path
output_path = 'output_file_easy.csv'  # Replace with your desired output file path

# Run the function with specified paths
process_and_save_data(input_path, output_path)
