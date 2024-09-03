import csv
import re

def extract_log_to_csv(log_path, csv_path):
    # Define a regex pattern to capture the timestamp and INFO content
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}):INFO:(.*)'
    
    # Open the log file and a new CSV file to write into
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

# Specify the path to your log file and the path where the CSV should be saved
log_file_path = r'E:\NFB_data_backup\20240821\log\audio_control_1724156156.5776126.log'
csv_file_path = 'output.csv'

# Call the function with the paths
extract_log_to_csv(log_file_path, csv_file_path)

# Print success message
print("Log data has been extracted and saved to CSV.")
