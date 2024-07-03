import pandas as pd

def merge_time_intervals(times):
    """ Merge overlapping time intervals and return a list of merged intervals. """
    if not times:
        return []

    # Sort intervals based on start time
    times.sort()
    merged = [times[0]]

    for current_start, current_end in times[1:]:
        last_start, last_end = merged[-1]

        # Check if there is an overlap
        if current_start <= last_end:
            # Merge intervals
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged

def extract_data_for_intervals(eeg_file_path, intervals):
    """ Extract EEG data for given time intervals from an EEG file. """
    # Load the EEG data
    eeg_data = pd.read_csv(eeg_file_path)

    # Filter data within each interval
    frames = []
    for start, end in intervals:
        mask = (eeg_data['timestamp_local'] >= start) & (eeg_data['timestamp_local'] <= end)
        frames.append(eeg_data[mask])

    return pd.concat(frames, ignore_index=True)

def extract_time_intervals(file_path):
    # Load the data
    data = pd.read_csv(file_path)
    
    # Get the time stamps
    time_stamps = data['TIME_STAMP']

    # Calculate start and end times with a 5-second window
    intervals = [(ts - 5, ts + 5) for ts in time_stamps]

    # Merge overlapping intervals
    merged_intervals = merge_time_intervals(intervals)

    return merged_intervals
def process_eeg_data(action_file_path, eeg_file_paths):
    # Extract time intervals from action data
    intervals = extract_time_intervals(action_file_path)

    # Extract data for each interval from each EEG file
    combined_eeg_data = pd.DataFrame()
    for eeg_file_path in eeg_file_paths:
        data = extract_data_for_intervals(eeg_file_path, intervals)
        combined_eeg_data = pd.concat([combined_eeg_data, data], ignore_index=True)

    # Remove potential duplicates after merging data from multiple files
    combined_eeg_data = combined_eeg_data.drop_duplicates().reset_index(drop=True)

    return combined_eeg_data

# Example usage:
action_file = '/Users/frank/Downloads/filtered_actions.csv'  # Path to the filtered actions CSV
eeg_files = ['/Volumes/T7/syr_20240628_lxk/2024-06-28_10_51_11trust_test3lxk_1.csv', '/Volumes/T7/syr_20240628_lxk/2024-06-28_11_38_19trust_test3lxk_2.csv']  # Paths to the EEG data files

# Process the EEG data
final_eeg_data = process_eeg_data(action_file, eeg_files)

# Save the combined EEG data to a new CSV file
final_eeg_data.to_csv('combined_eeg_data.csv', index=False)
print("Data saved to 'combined_eeg_data.csv'.")
