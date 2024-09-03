import csv
import re
import os

def extract_log_to_csv(log_folder, output_folder):
    # Define a regex pattern to capture the timestamp and INFO content
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}):INFO:(.*)'
    
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each log file in the folder
    for file_name in os.listdir(log_folder):
        if file_name.endswith('.log'):
            log_path = os.path.join(log_folder, file_name)
            csv_path = os.path.join(output_folder, file_name.replace('.log', '.csv'))

            with open(log_path, 'r') as log_file, open(csv_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write header to CSV
                csv_writer.writerow(['Timestamp', 'Info Content'])
                
                # Read each line of the log file
                for line in log_file:
                    # Use regex to find matches
                    match = re.match(pattern, line)
                    if match:
                        # Extract the timestamp and INFO content from the match
                        timestamp, info_content = match.groups()
                        # Write the extracted data to CSV
                        csv_writer.writerow([timestamp, info_content])

# Specify the path to your log folder and the output folder for CSV files
log_folder_path = r'E:\NFB_data_backup\20240821\log'
output_folder_path = r'E:\NFB_data_backup\20240821\csv'

# Call the function with the folder paths
extract_log_to_csv(log_folder_path, output_folder_path)

# Print success message
print("All log data has been extracted and saved to CSV files.")
