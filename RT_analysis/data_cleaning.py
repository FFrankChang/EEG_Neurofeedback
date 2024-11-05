import pandas as pd

def process_events_complete(df):
    df['timestamp_mo'] = pd.to_datetime(df['timestamp'], unit='s')
    df.sort_values('timestamp_mo', inplace=True)
    df['diff_seconds'] = df['timestamp_mo'].diff().dt.total_seconds()
    last_true_index = None
    modified_count = 0
    modified_timestamps = []
    modified_index = []

    for i in df.index:
        if df.at[i, 'event_triggered']:
            if last_true_index is None or (df.at[i, 'timestamp_mo'] - df.at[last_true_index, 'timestamp_mo']).total_seconds() >= 3:
                last_true_index = i
            else:
                df.at[i, 'event_triggered'] = False
                modified_count += 1
                modified_timestamps.append(df.at[i, 'timestamp_mo'])
                modified_index.append(i)
    df.drop(columns=['diff_seconds'], inplace=True)
    
    return modified_count, modified_timestamps,modified_index

# Load the CSV file
data_path = r"G:\Exp_V0_data\S02\C04_traffic_20241022_105607.csv"
data = pd.read_csv(data_path)

# Clean the data
modified_count, modified_timestamps, modified_index = process_events_complete(data)

print(f"Number of modifications: {modified_count}")
print("Modified timestamps:", modified_timestamps)
print("Modified index:", modified_index)

# Save the cleaned data
data.to_csv('cleaned_data.csv', index=False)
