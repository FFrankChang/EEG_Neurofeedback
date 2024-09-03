import pandas as pd
import os
from datetime import datetime

# Define the directory containing the CSV files (adjust this path as necessary)
directory = r'E:\NFB_data_backup\filtered\S09_D03'

# Initialize a DataFrame to store the summary information
summary_df = pd.DataFrame(columns=['segmentStart', 'segmentEnd', 'segmentName', 'segmentSource'])

# Function to parse the datetime and C01/C02 from the filename
def parse_details_from_filename(filename):
    day = filename.split('_')[3]
    date_str = filename.split('_')[5].split('.')[0]
    datetime_parsed = datetime.strptime(date_str, '%Y%m%d%H%M%S')
    c_code = 'C01' if 'C01' in filename else 'C02' if 'C02' in filename else None
    return datetime_parsed, c_code , day

# Function to get the segment start time based on the C01 or C02 condition
def get_segment_start(df, c_code):
    if c_code == 'C01':
        # Get the timestamp where TOR is "Yes"
        return df[df['TOR'] == 'Yes']['timestamp'].iloc[0]
    elif c_code == 'C02':
        # Get the timestamp where TOR changes from "False" to "True"
        return df[df['TOR'] == True]['timestamp'].iloc[0]

# List and sort the CSV files based on the datetime embedded in their filenames
files = [f for f in os.listdir(directory) if 'carla' in f and f.endswith('.csv') and ('C01' in f or 'C02' in f)]
files.sort(key=lambda x: parse_details_from_filename(x)[0])
data_rows = []

# Process each file
for index, filename in enumerate(files, start=1):
    # Determine segment type and C01/C02 from filename
    datetime_parsed, c_code , day= parse_details_from_filename(filename)
    segment_type = 'feedback' if 'feedback' in filename else 'silence' if 'silence' in filename else None
    if segment_type is None:
        continue  # Skip files that do not match the expected pattern

    # Read the CSV file
    df = pd.read_csv(os.path.join(directory, filename))
    time_column = 'timestamp' if 'timestamp' in df.columns else 'Time' if 'Time' in df.columns else None
    if time_column is None:
        continue  # Skip files that do not have a valid time column

    # Extract the segment start and end timestamps based on conditions
    segment_start = get_segment_start(df, c_code)
    segment_end = segment_start + 30

    # Create a dictionary for the current row and append to the list
    row = {
        'segmentStart': segment_start,
        'segmentEnd': segment_end,
        'segmentName': f"{str(index).zfill(2)}_{c_code}_{segment_type}_{day}",
        'segmentSource': 'smartEye'
    }
    data_rows.append(row)

# Convert list of dictionaries to DataFrame
summary_df = pd.DataFrame(data_rows)

# Save the summary to a new CSV file
summary_df.to_csv('S09_D03_segment.csv', index=False)

