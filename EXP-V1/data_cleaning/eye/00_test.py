import pandas as pd
from scipy.spatial import KDTree

def load_data(file_a_path, file_b_path):
    # Load File A and File B
    file_a = pd.read_csv(file_a_path)
    file_b = pd.read_csv(file_b_path)
    return file_a, file_b

def find_nearest_time_ms(timestamp, timestamp_tree, file_b):
    # Find the closest time in file B to the given timestamp and convert to seconds
    distance, index = timestamp_tree.query([timestamp])
    return file_b.loc[index, 'time_ms'] / 1000  # Convert milliseconds to seconds

def update_timestamps(file_a, file_b):
    # Create a KDTree for efficient nearest timestamp search
    timestamp_tree = KDTree(file_b[['timestamp']].values)
    
    # Update segmentStart and segmentEnd in file A, results converted to seconds
    file_a['segmentStart'] = file_a['segmentStart'].apply(lambda x: find_nearest_time_ms(x, timestamp_tree, file_b))
    file_a['segmentEnd'] = file_a['segmentEnd'].apply(lambda x: find_nearest_time_ms(x, timestamp_tree, file_b))
    return file_a

# Main execution code
def main():
    Subject ="S10"
    day = "D03" 
    test = Subject+"_" + day
    file_a_path = rf'E:\NFB_data_backup\filtered\{test}\{test}_segment.csv'  # Replace with your File A path
    file_b_path = rf'E:\NFB_data_backup\filtered\{test}\{test}_eye_data.csv'  # Replace with your File B path

    # Load data
    file_a, file_b = load_data(file_a_path, file_b_path)
    
    # Update timestamps
    updated_file_a = update_timestamps(file_a, file_b)
    
    # Save the updated File A back to the original location
    updated_file_a.to_csv(file_a_path, index=False)
    
    print("File A has been updated and saved.")

# Run main function
if __name__ == '__main__':
    main()
