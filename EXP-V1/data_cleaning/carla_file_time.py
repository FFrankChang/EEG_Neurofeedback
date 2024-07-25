import os
from datetime import datetime

# Specify the path to the directory containing the folders
path_to_directories = r'F:\NFB_EXP\Exp_V1_data\filtered'

def rename_files(directory):
    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a CSV and contains 'carla'
            if file.endswith('.csv') and 'carla' in file:
                # Split the filename from the extension
                base_name, extension = os.path.splitext(file)
                
                # Split the base part of the filename into components
                parts = base_name.split('_')
                timestamp_part = None
                for part in parts:
                    # Check if this part could be a timestamp by checking for digits and a decimal point
                    if '.' in part :
                        timestamp_part = part
                        break
                
                # If a timestamp part is found, try to convert and rename
                if timestamp_part:
                    # Try to extract the timestamp, assuming it includes milliseconds
                    try:
                        # Split the part into seconds and milliseconds based on the decimal
                        seconds, milliseconds = timestamp_part.split('.')
                        # Convert seconds and milliseconds to a datetime object
                        original_timestamp = datetime.fromtimestamp(int(seconds))
                        formatted_date = original_timestamp.strftime('%Y%m%d%H%M%S')
                        # Add milliseconds to the formatted string
                        formatted_date += milliseconds[:3]  # Assumes milliseconds are the first 3 digits after the decimal
                        new_filename = base_name.replace(timestamp_part, formatted_date) + extension
                        
                        # Full path for old and new file
                        old_file_path = os.path.join(root, file)
                        new_file_path = os.path.join(root, new_filename)
                        
                        # Rename the file
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed {old_file_path} to {new_file_path}")
                    except Exception as e:
                        print(f"Skipping {file}: {e} - timestamp conversion issue.")

# Start the renaming process
rename_files(path_to_directories)
print("All relevant files have been renamed.")
