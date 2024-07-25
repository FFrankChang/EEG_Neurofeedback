import os
import pandas as pd

def rename_column_in_csv(directory):
    # Traverse the directory recursively
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a CSV and contains 'carla_c02'
            if file.endswith('.csv') and 'carla_c02' in file:
                file_path = os.path.join(root, file)
                try:
                    # Load the CSV file
                    df = pd.read_csv(file_path)

                    # Check if the 'Time' column is in the DataFrame
                    if 'Time' in df.columns:
                        # Rename the 'Time' column to 'timestamp'
                        df.rename(columns={'Time': 'timestamp'}, inplace=True)

                        # Save the modified DataFrame back to CSV
                        df.to_csv(file_path, index=False)
                        print(f"Column renamed in {file_path}")
                    else:
                        print(f"No 'Time' column in {file_path}")
                except pd.errors.EmptyDataError:
                    print(f"Skipping empty CSV file: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Specify the path to the directory containing the folders
path_to_directories = r'F:\NFB_EXP\Exp_V1_data\filtered'
rename_column_in_csv(path_to_directories)
