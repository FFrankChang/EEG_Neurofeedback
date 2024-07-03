import pandas as pd
import numpy as np

# Load the data from the CSV file
data = pd.read_csv('/Users/frank/Projects/EEG_Neurofeedback/combined_eeg_data.csv')

# Drop the 'Timestamp_EEG' column
data.drop(columns=['Timestamp_EEG'], inplace=True)

# Assuming that the data in 'Sample' column is stored as a string representation of a list
data['Sample'] = data['Sample'].apply(lambda x: np.fromstring(x.strip('[]'), sep=', '))

# Define the column names for the expanded data
column_names = ['Fp1', 'Fpz', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6',
                'M1', 'T7', 'C3', 'Cz', 'C4', 'T8', 'M2', 'CP5', 'CP1', 'CP2', 'CP6', 'P7', 
                'P3', 'Pz', 'P4', 'P8', 'POz', 'O1', 'Oz', 'O2', 'BIP 01', 'STATUS', 'COUNTER', 
                'machine_timestamp']

# Split the array in 'Sample' into separate columns
expanded_data = pd.DataFrame(data['Sample'].tolist(), columns=column_names)

# Combine the expanded data with the original dataframe minus the 'Sample' column
processed_data = pd.concat([data.drop(columns=['Sample']), expanded_data], axis=1)

# Save the processed data to a new CSV file
processed_data.to_csv('processed_output.csv', index=False)

print("Data processing completed and saved to 'processed_output.csv'.")
