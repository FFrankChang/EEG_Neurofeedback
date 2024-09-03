import pandas as pd
import glob
import os

def calculate_acceleration(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Convert timestamps to datetime and sort the data
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    data = data.sort_values(by='timestamp')
    
    # Calculate differences in speed and time
    data['Time_Difference'] = data['timestamp'].diff().dt.total_seconds()
    data['Speed_Difference'] = data['Speed'].diff()
    
    # Calculate acceleration and update the column
    data['Acceleration'] = data['Speed_Difference'] / data['Time_Difference']
    data['Acceleration'].fillna(0, inplace=True)  # Fill NaN values in the first row

    # Save the updated data back to the original CSV file
    data.to_csv(file_path, index=False)
    print("File updated:", file_path)

def process_files(directory):
    # Build the search pattern
    search_pattern = os.path.join(directory, '**/*carla*C02*.csv')
    
    # Find all matching CSV files
    files = glob.glob(search_pattern, recursive=True)
    
    # Process each file
    for file_path in files:
        # Calculate and save acceleration directly to the same file
        calculate_acceleration(file_path)

# Example usage
directory = r'E:\NFB_data_backup\filtered'
process_files(directory)
