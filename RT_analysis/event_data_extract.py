import os
import pandas as pd

def extract_and_save_csv_data(folder_path):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            all_data = pd.DataFrame()

            for filename in os.listdir(subfolder_path):
                if filename.endswith(".csv") and "C04" in filename:
                    file_path = os.path.join(subfolder_path, filename)
                    data = pd.read_csv(file_path)
                    filtered_data = data[data['event_triggered'] == True]

                    extracted_data = filtered_data[['timestamp', 'event_value','reaction_time_2','reaction_time_3','reaction_time_4','reaction_time_5','reaction_time_8','reaction_time_10']]

                    if 'simple' in filename.lower():
                        extracted_data['scenario'] = 'simple'
                    elif 'traffic' in filename.lower():
                        extracted_data['scenario'] = 'traffic'
                    extracted_data['subject'] = subfolder

                    all_data = pd.concat([all_data, extracted_data], ignore_index=True)

            if not all_data.empty:
                new_filename = f"{subfolder}_event_time.csv"
                new_file_path = os.path.join(subfolder_path, new_filename)
                all_data.to_csv(new_file_path, index=False)
                print(f"Saved: {new_file_path}")

folder_path = r'G:\Exp_V0_data\data'  
extract_and_save_csv_data(folder_path)
