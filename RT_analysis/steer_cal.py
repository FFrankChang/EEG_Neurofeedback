import os
import pandas as pd

def process_and_save_csv_data(folder_path):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".csv") and "C04" in filename:
                    file_path = os.path.join(subfolder_path, filename)
                    data = pd.read_csv(file_path)
                    data['steer_angle'] = (data['steer'] * 540).round(3)
                    data.to_csv(file_path, index=False)
                    print(f"Processed and saved: {file_path}")

folder_path = r'G:\Exp_V0_data\data'  
process_and_save_csv_data(folder_path)
