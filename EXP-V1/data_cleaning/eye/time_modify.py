import pandas as pd

# Load the CSV file
file_path = r'E:\NFB_data_backup\eye_extract\S05_D01_eye_data.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Define the base time and the offset
base_time = 796027548
offset = 727766

# Identify rows where time_ms is greater than the base time
mask = data['time_ms'] > base_time

# Apply the transformation to these rows
data.loc[mask, 'time_ms'] = data.loc[mask, 'time_ms'] - base_time + offset

# Save the modified data back to a new CSV file if needed
data.to_csv('S05_D01_eye_data.csv', index=False)  # This will save the modified data

# Optionally, you can display the top rows to check the data
print(data.head())
