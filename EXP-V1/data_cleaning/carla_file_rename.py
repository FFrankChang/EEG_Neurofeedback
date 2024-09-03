import os

# Specify the path to the directory containing the folders
path_to_directories = r'E:\NFB_data_backup\filtered'

# Mapping to replace parts of file names
replacement_map = {
    'c01': 'C01',
    'c02': 'C02'
}

def rename_files(directory):
    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a CSV and contains 'carla'
            if file.endswith('.csv') and 'carla' in file:
                # Replace parts of the file name based on the replacement_map
                new_name = file
                for old_part, new_part in replacement_map.items():
                    new_name = new_name.replace(old_part, new_part)
                
                # Full path for old and new file
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed {old_file_path} to {new_file_path}")

# Start the renaming process
rename_files(path_to_directories)
print("All relevant files have been renamed.")
