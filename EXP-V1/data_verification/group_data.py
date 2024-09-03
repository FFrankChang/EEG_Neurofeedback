import pandas as pd
import numpy as np

# Load the dataset
file_path = r'E:\NFB_data_backup\results\final_results_20s.csv'
data = pd.read_csv(file_path)

# Function to assign group labels
def assign_group(sub_df):
    # Shuffle the subgroup
    shuffled_df = sub_df.sample(frac=1, random_state=42).reset_index(drop=True)
    # Split into two groups
    mid_point = len(shuffled_df) // 2
    shuffled_df['Lable'] = ['A'] * mid_point + ['B'] * (len(shuffled_df) - mid_point)
    return shuffled_df

# Group the data and apply the function
grouped_data = data.groupby(['Subject', 'Day', 'Condition']).apply(assign_group).reset_index(drop=True)

# Save the updated dataset
grouped_data.to_csv('updated_final_results.csv', index=False)

# Output a preview and the new group counts
print(grouped_data[['Subject', 'Day', 'Condition', 'Lable']].head())
print(grouped_data['Lable'].value_counts())
