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

# Suppose the file path of the filtered CSV is 'filtered_actions.csv'
time_intervals = extract_time_intervals('/Users/frank/Downloads/filtered_actions.csv')

# Print the required time intervals
for start, end in time_intervals:
    print(f"Start: {start}, End: {end}")
