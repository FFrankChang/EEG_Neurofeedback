import pandas as pd
import os

def analyze_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Basic counts
    total_rows = len(data)
    traffic_count = data[data['scenario'] == 'traffic'].shape[0]
    simple_count = data[data['scenario'] == 'simple'].shape[0]

    # Columns of interest for missing data
    columns_of_interest = [
        'reaction_time_2', 'reaction_time_3', 'reaction_time_4', 
        'reaction_time_5', 'reaction_time_8', 'reaction_time_10'
    ]

    # Calculate missing values and their percentages
    missing_data = data[columns_of_interest].isna().sum()
    missing_percentage = (missing_data / total_rows) * 100

    # Prepare the results
    summary = {
        'File': os.path.basename(file_path),  
        'Total Rows': total_rows,
        'Traffic Rows': traffic_count,
        'Simple Rows': simple_count
    }
    for col, missing in missing_data.items():
        summary[f'{col} Missing Count'] = missing
        summary[f'{col} Missing Percentage (%)'] = missing_percentage[col]
    
    return summary

def batch_process(folder_path):
    summaries = []
    # Traverse subfolders like S01, S02, etc.
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            # Process each CSV file in the subfolder
            for file in os.listdir(subfolder_path):
                if 'event' in file and file.endswith('.csv'):
                    file_path = os.path.join(subfolder_path, file)
                    summary = analyze_data(file_path)
                    summaries.append(summary)

    # Convert summaries to DataFrame
    results_df = pd.DataFrame(summaries)
    # Rearrange columns to put 'File' at the first position
    cols = ['File'] + [col for col in results_df.columns if col != 'File']
    results_df = results_df[cols]
    # Save to a new CSV file
    results_df.to_csv( 'summary_results.csv', index=False)

# Example usage
folder_path = r'G:\Exp_V0_data\data'
batch_process(folder_path)
