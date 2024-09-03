import pandas as pd

def process_data(file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Grouping the data by 'Subject', 'Day', and 'Condition'
    grouped_data = data.groupby(['Subject', 'Day', 'Condition', 'Group']).agg({
        'Min_TTC': 'mean',
        'Steering_Angle_STD': 'mean',
        'Acceleration_x_Mean': 'mean',
        'Acceleration_x_STD': 'mean',
        'Acceleration_x_Change_Rate_Mean': 'mean',
        'Road_Exits': 'mean',
        'Average_Lanes_Per_Change': 'mean',
        'Successful_Changes': 'mean',
        'Total_Successful_Change_Time': 'mean'
    }).reset_index()

    # Save the processed data to a new CSV file
    output_file_path = file_path.replace('.csv', '_grouped.csv')
    grouped_data.to_csv(output_file_path, index=False)
    
    return output_file_path

# Specify the file path to your CSV file
file_path = r'E:\NFB_data_backup\results\test_01\final_results_10s.csv'  # Replace this with the path to your CSV file

# Process the data
output_file = process_data(file_path)
print(f'Grouped data saved to: {output_file}')
