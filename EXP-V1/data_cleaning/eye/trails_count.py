

import pandas as pd
import os

# Define the directory where the CSV files are stored
directory = r'E:\NFB_data_backup\eye_extract'

# Define the segment names of interest
segments = ['C01_feedback', 'C01_silence', 'C02_feedback', 'C02_silence']

# Initialize a list to collect counts from all files
all_counts = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv") and 'segment' in filename:
        # Load the CSV file
        data = pd.read_csv(os.path.join(directory, filename))

        # Initialize a dictionary to count occurrences in the current file
        counts = {segment: 0 for segment in segments}
        
        # Count occurrences using exact string matching within 'segmentName'
        for segment in segments:
            pattern = f'.*{segment}.*'
            counts[segment] = data['segmentName'].str.contains(pattern).sum()

        # Add the counts dictionary to the list
        all_counts.append(counts)
        
        # Output the count for each file
        print(f"Counts for {filename}:", counts)

# Convert the list of dictionaries to a DataFrame
df_counts = pd.DataFrame(all_counts)

# Calculate minimum and average for each segment across all files
min_values = df_counts.min()
mean_values = df_counts.mean()

# Print the results
print( min_values)
print( mean_values)
