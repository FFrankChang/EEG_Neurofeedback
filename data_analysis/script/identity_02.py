import pandas as pd

# Load the data
data_path = r"D:\gitee\EEG_Neurofeedback\data\20240529_syr_09_hard_silence\carla_merged.csv"  # Adjust to your actual file path
carla_data = pd.read_csv(data_path)

# Process 'Mode_Switched' to identify manual control activation
carla_data['Mode_Switched'] = carla_data['Mode_Switched'].fillna("No")
switch_indices = carla_data.index[carla_data['Mode_Switched'].eq("Yes")]

# List to store the deceleration periods
deceleration_periods = []

# Analyze data after each switch to manual control
for index in switch_indices:
    subset = carla_data.loc[index:].reset_index(drop=True)
    below_threshold = subset['Lead_Vehicle_Speed'] < 78

    in_deceleration = False
    start_time = None
    for i, (time, speed, is_below) in enumerate(zip(subset['timestamp'], subset['Lead_Vehicle_Speed'], below_threshold)):
        if is_below and not in_deceleration:
            in_deceleration = True
            start_time = time
        elif not is_below and in_deceleration:
            in_deceleration = False
            if start_time:
                deceleration_periods.append((start_time, subset['timestamp'][i-1]))

# Process the first 5 deceleration periods
for start, end in deceleration_periods[:5]:
    # Extend end time by 3 seconds
    end_extended = end + 3
    
    # Filter data within the deceleration period
    deceleration_data = carla_data[(carla_data['timestamp'] >= start) & (carla_data['timestamp'] <= end_extended)]
    
    # Calculate statistics for 'Steering_Angle'
    steering_angles = deceleration_data['Steering_Angle']
    mean_change_rate = steering_angles.diff().mean()
    variance = steering_angles.var()
    coefficient_of_variation = steering_angles.std() / steering_angles.mean()

    print(f"Deceleration from {start} to {end_extended} (extended):")
    print(f"Mean Change Rate: {mean_change_rate}")
    print(f"Variance: {variance}")
    print(f"Coefficient of Variation: {coefficient_of_variation}")
