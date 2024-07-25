import pandas as pd
import os
from datetime import datetime

# Define the directory containing the CSV files (adjust this path as necessary)
directory = r'F:\NFB_EXP\Exp_V1_data\filtered\syh_D03'

# Initialize a DataFrame to store the summary information
summary_df = pd.DataFrame(columns=['segmentStart', 'segmentEnd', 'segmentName', 'segmentSource'])

# Function to parse the datetime from the filename
def parse_datetime_from_filename(filename):
    date_str = filename.split('_')[5].split('.')[0]
    return datetime.strptime(date_str, '%Y%m%d%H%M%S')

# List and sort the CSV files based on the datetime embedded in their filenames
files = [f for f in os.listdir(directory) if 'carla' in f and f.endswith('.csv')]
files.sort(key=parse_datetime_from_filename)
data_rows = []
# Process each file
for index, filename in enumerate(files, start=1):
    # Determine segment type based on the filename
    if 'feedback' in filename:
        segment_type = 'feedback'
    elif 'silence' in filename:
        segment_type = 'silence'
    else:
        continue  # Skip files that do not match the expected pattern

    # Read the CSV file
    df = pd.read_csv(os.path.join(directory, filename))
    time_column = 'timestamp' if 'timestamp' in df.columns else 'Time' if 'Time' in df.columns else None

    # Extract timestamps
    segment_start = df[time_column].iloc[0]
    segment_end = df[time_column].iloc[-1]
    # Create a dictionary for the current row and append to the list
    row = {
        'segmentStart': segment_start,
        'segmentEnd': segment_end,
        'segmentName': f"{str(index).zfill(2)}_{segment_type}",
        'segmentSource': 'smartEye'
    }
    data_rows.append(row)

# Convert list of dictionaries to DataFrame
summary_df = pd.DataFrame(data_rows)

# Save the summary to a new CSV file
summary_df.to_csv('S03_segment.csv', index=False)

print("Summary CSV has been created successfully.")
