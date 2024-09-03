import pandas as pd
import numpy as np
import os

# Set the folder path
folder_path = r'E:\NFB_data_backup\results\test_01'

# Function to assign labels to each CSV file and save
def assign_group_and_save(file_path):
    # Read the data
    data = pd.read_csv(file_path)
    
    # Function to assign labels
    def assign_group(sub_df):
        shuffled_df = sub_df.sample(frac=1, random_state=42).reset_index(drop=True)
        mid_point = len(shuffled_df) // 2
        shuffled_df['Label'] = ['A'] * mid_point + ['B'] * (len(shuffled_df) - mid_point)
        return shuffled_df

    # Apply the grouping function and reset the index
    grouped_data = data.groupby(['Subject', 'Day', 'Condition']).apply(assign_group).reset_index(drop=True)

    # Combine 'Subject' and 'Label' into a new 'Subject' column, then drop 'Label'
    grouped_data['Subject'] = grouped_data['Subject'] + grouped_data['Label']
    grouped_data.drop(columns='Label', inplace=True)

    # Save the modified data back to the original file
    grouped_data.to_csv(file_path, index=False)

# Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(f'Processing file: {filename}')
        assign_group_and_save(file_path)
