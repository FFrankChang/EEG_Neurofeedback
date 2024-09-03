import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(file_path, data, column_name, take_over_time, multiplier=1):
    plt.figure()
    plt.plot(data['timestamp'], data[column_name] * multiplier, label=column_name)
    plt.xlabel('Timestamp')
    plt.ylabel(column_name)
    plt.title(f'{os.path.basename(file_path)} {column_name}')

    if pd.notna(take_over_time):
        plt.axvline(x=take_over_time, color='lightcoral', linestyle='--', label='Take Over Time')
    plt.legend()
    plt.savefig(file_path.replace('.csv', '.png'))
    plt.close()

def process_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        results_path = os.path.join(subdir, 'updated_carla_results.csv')
        if os.path.isfile(results_path):
            results_df = pd.read_csv(results_path)
            for idx, row in results_df.iterrows():
                file_name = row.iloc[0]
                file_path = os.path.join(subdir, file_name)
                if os.path.isfile(file_path):
                    data = pd.read_csv(file_path)
                    data = data[(data['timestamp'] >= row['TOR Time']) & (data['timestamp'] <= row['Last Time'])]
                    if 'C01' in file_name and 'Steering_Angle' in data.columns:
                        plot_data(file_path, data, 'Steering_Angle', row['take over time'])
                    elif 'C02' in file_name and 'Steering' in data.columns:
                        plot_data(file_path, data, 'Steering', row['take over time'], multiplier=540)
                    else:
                        print(f"Relevant columns not found in {file_name}.")
                else:
                    print(f"File {file_name} not found in {subdir}.")

root_directory = r'E:\NFB_data_backup\20240730'
process_files(root_directory)
