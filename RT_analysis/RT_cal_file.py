import pandas as pd
import os

def process_csv(file_path):
    df = pd.read_csv(file_path)
    df['event_triggered'] = df['event_triggered'].astype(bool)

    for angle in  [2, 3, 4, 5, 8, 10]:
        df[f'reaction_time_{angle}'] = None

    event_indices = df[df['event_triggered']].index

    for i in range(len(event_indices) - 1):
        start_idx = event_indices[i]
        end_idx = event_indices[i + 1]
        start_angle = df.loc[start_idx, 'steer_angle']
        
        recorded = {angle: False for angle in [2, 3, 4, 5, 8, 10]}
        for idx in range(start_idx + 1, end_idx):
            current_angle = df.loc[idx, 'steer_angle']
            for angle in  [2, 3, 4, 5, 8, 10]:
                if abs(current_angle - start_angle) >= angle and not recorded[angle]:
                    df.loc[start_idx, f'reaction_time_{angle}'] = df.loc[idx, 'timestamp'] - df.loc[start_idx, 'timestamp']
                    recorded[angle] = True

    df.to_csv(file_path, index=False)

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if 'C04' in file and file.endswith('.csv'):
                process_csv(os.path.join(root, file))

folder_path = r'G:\Exp_V0_data\data'
process_folder(folder_path)
