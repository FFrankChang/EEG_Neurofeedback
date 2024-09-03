import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_processed_arousal_from_csv(root_dir, save_dir):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Walk through all directories and files in the root directory
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if 'psd' in file.lower() and file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                try:
                    # Load the CSV file
                    df = pd.read_csv(file_path)

                    # Process and plot all columns that include 'arousal' in their name
                    for column in df.columns:
                        if 'arousal' in column.lower():
                            # Convert arousal values to 0 or 1
                            df[column] = (df[column] > 0.6).astype(int)
                            
                            # Plotting
                            plt.figure()
                            df[column].plot(title=f"Processed {column}")
                            plt.xlabel('Index')
                            plt.ylabel('Value ')

                            # Save the plot to the specified directory
                            plt.savefig(os.path.join(save_dir, f"{os.path.splitext(file)[0]}_processed_{column}.png"))
                            plt.close()
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

# Example usage
plot_processed_arousal_from_csv(r'E:\NFB_data_backup\pre_nfb_raw_data', r'E:\NFB_data_backup\arousal')
