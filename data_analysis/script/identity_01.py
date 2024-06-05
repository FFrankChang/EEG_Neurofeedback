import pandas as pd

# Load the data
data_path = r"D:\gitee\EEG_Neurofeedback\data\20240529_syr_09_hard_silence\carla_20240529120834.csv"  # Change this to your actual file path
carla_data = pd.read_csv(data_path)

# Process 'Mode_Switched' to mark the manual driving mode
carla_data['Mode_Switched'] = carla_data['Mode_Switched'].fillna("No")

# Find indices where 'Mode_Switched' changes to "Yes"
switch_indices = carla_data.index[carla_data['Mode_Switched'].eq("Yes")]

# List to store the deceleration periods
continuous_deceleration_periods = []

# Analyze data after each switch to manual control
for index in switch_indices:
    # Data subset from the point where the mode switched
    subset = carla_data.loc[index:].reset_index(drop=True)
    
    # Check for Lead_Vehicle_Speed being continuously less than 78
    speed_less_than_78 = subset['Lead_Vehicle_Speed'] < 78
    
    # Find start and end of each deceleration period
    in_deceleration = False
    start_time = None
    for i, (time, speed, is_below_threshold) in enumerate(zip(subset['timestamp'], subset['Lead_Vehicle_Speed'], speed_less_than_78)):
        if is_below_threshold and not in_deceleration:
            # Start of a new deceleration period
            in_deceleration = True
            start_time = time
        elif not is_below_threshold and in_deceleration:
            # End of the current deceleration period
            in_deceleration = False
            if start_time:
                continuous_deceleration_periods.append((start_time, subset['timestamp'][i-1]))

# Handle the case where the deceleration period might still be ongoing at the end of the data
if in_deceleration and start_time:
    continuous_deceleration_periods.append((start_time, subset['timestamp'].iloc[-1]))

# Output the detected deceleration periods
for start, end in continuous_deceleration_periods:
    print(f"Deceleration from {start} to {end}")
