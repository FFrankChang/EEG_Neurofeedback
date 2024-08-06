import pandas as pd

# Load the CSV file
file_path = r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\C01_control_D01_max.csv'
data = pd.read_csv(file_path)

# Group by the 'sub' column and select the first three rows for each group
filtered_data = data.groupby('sub').head(3)

# Save the filtered data to a new CSV file
filtered_file_path = r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\filtered\C01_control_D01_max.csv'
filtered_data.to_csv(filtered_file_path, index=False)
