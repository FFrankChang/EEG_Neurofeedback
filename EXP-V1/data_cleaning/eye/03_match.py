import pandas as pd
import os
from scipy.spatial import KDTree

def load_data(folder_path):
    # Initialize paths
    file_a_path, file_b_path = None, None
    
    # Check for files that match the criteria in the folder
    for file_name in os.listdir(folder_path):
        if 'segment' in file_name and file_name.endswith('.csv'):
            file_a_path = os.path.join(folder_path, file_name)
        elif 'eye_data' in file_name and file_name.endswith('.csv'):
            file_b_path = os.path.join(folder_path, file_name)
    
    if not file_a_path or not file_b_path:
        return None, None
    else:
        file_a = pd.read_csv(file_a_path)
        file_b = pd.read_csv(file_b_path)
        return file_a, file_b

def find_nearest_time_ms(timestamp, timestamp_tree, file_b):
    # Find the closest time in file B to the given timestamp and convert to seconds
    distance, index = timestamp_tree.query([timestamp], k=1)
    if distance == float('inf'):
        return None
    else:
        return file_b.loc[index[0], 'time_ms'] / 1000

def update_timestamps(file_a, file_b):
    # Create a KDTree for efficient nearest timestamp search
    timestamp_tree = KDTree(file_b[['timestamp']].values)
    
    # Update segmentStart and segmentEnd in file A, results converted to seconds
    file_a['segmentStart'] = file_a['segmentStart'].apply(lambda x: find_nearest_time_ms(x, timestamp_tree, file_b))
    file_a['segmentEnd'] = file_a['segmentEnd'].apply(lambda x: find_nearest_time_ms(x, timestamp_tree, file_b))
    
    if file_a['segmentStart'].isnull().any() or file_a['segmentEnd'].isnull().any():
        return None
    else:
        return file_a

def process_folders(root_path):
    for folder_name in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder_name)
        if os.path.isdir(folder_path):
            file_a, file_b = load_data(folder_path)
            if file_a is None or file_b is None:
                print(f"Missing files in {folder_name}. Skipping...")
                continue
            
            updated_file_a = update_timestamps(file_a, file_b)
            if updated_file_a is not None:
                file_a_path = [f for f in os.listdir(folder_path) if 'segment' in f and f.endswith('.csv')]
                updated_file_a.to_csv(os.path.join(folder_path, file_a_path[0]), index=False)
                print(f"Processed and updated {folder_name}.")
            else:
                print(f"Timestamps not found in {folder_name}. Skipping...")

# Main execution code
if __name__ == '__main__':
    root_path = r'E:\NFB_data_backup\test'  # Path to the root directory containing all folders
    process_folders(root_path)
