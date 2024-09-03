import pandas as pd
import os

# Specify the directory containing the CSV files
directory = r'E:\NFB_data_backup\results'  # Replace with your directory path

# Define a function to determine the group based on the Subject ID
def classify_subject(subject_id):
    if subject_id in ['S01', 'S02', 'S03', 'S04', 'S05']:
        return 'BCI'
    elif subject_id in ['S06', 'S07', 'S08', 'S09', 'S10']:
        return 'Sham'
    else:
        return 'Unknown'  # Just in case there are unexpected Subject IDs

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Apply the function to create a new column
        df['Group'] = df['Subject'].apply(classify_subject)
        
        # Save the modified DataFrame back to the same CSV file
        df.to_csv(file_path, index=False)
        
        print(f"Updated file saved: {file_path}")
