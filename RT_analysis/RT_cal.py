import pandas as pd

df = pd.read_csv(r"G:\Exp_V0_data\data\S21_C04_tracffic_20241031_110000.csv")

df['event_triggered'] = df['event_triggered'].astype(bool)

for angle in [2, 3, 4, 5]:
    df[f'reaction_time_{angle}'] = None

event_indices = df[df['event_triggered']].index

for i in range(len(event_indices) - 1):
    start_idx = event_indices[i]
    end_idx = event_indices[i + 1]
    start_angle = df.loc[start_idx, 'steer_angle']
    
    recorded = {angle: False for angle in [2, 3, 4, 5]}
    for idx in range(start_idx + 1, end_idx):
        current_angle = df.loc[idx, 'steer_angle']
        for angle in [2, 3, 4, 5]:
            if abs(current_angle - start_angle) >= angle and not recorded[angle]:
                df.loc[start_idx, f'reaction_time_{angle}'] = df.loc[idx, 'timestamp'] - df.loc[start_idx, 'timestamp']
                recorded[angle] = True

df.to_csv('updated_file.csv', index=False)
