import pandas as pd
from scipy.stats import spearmanr
import os

def process_file(file_path):
    data = pd.read_csv(file_path)
    first_switch_index = data[data['Mode_Switched'] == 'Yes'].index.min()

    if pd.notna(first_switch_index):
        filtered_data = data.loc[first_switch_index:]
        cleaned_data = filtered_data.dropna(subset=['arousal', 'Lead_Vehicle_Speed'])

        # Calculate Spearman's rank correlation coefficient and p-value
        if not cleaned_data.empty:
            spearman_result = spearmanr(cleaned_data['arousal'], cleaned_data['Lead_Vehicle_Speed'])
            return spearman_result.correlation, spearman_result.pvalue
    return None, None

def main():
    base_path = r"E:\NFB_data_backup\data_20240606\test"
    results = []

    # Iterate over all directories in the base path
    for dir_name in os.listdir(base_path):
        dir_path = os.path.join(base_path, dir_name)
        if os.path.isdir(dir_path):
            file_path = os.path.join(dir_path, 'carla_merged.csv')
            if os.path.exists(file_path):
                correlation, pvalue = process_file(file_path)
                if correlation is not None:
                    results.append({'Directory': dir_name, 'Correlation': correlation, 'P-value': pvalue})

    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(r"E:\NFB_data_backup\data_20240606\test\summary_results.csv", index=False)
    print("Results saved to summary_results.csv")

if __name__ == "__main__":
    main()
