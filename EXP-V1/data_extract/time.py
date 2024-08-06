import pandas as pd

def fill_missing_values(carla_data):
    """Fill missing values in the 'Mode_Switched' column."""
    carla_data['Mode_Switched'] = carla_data['Mode_Switched'].fillna("No")
    return carla_data

def detect_deceleration_periods(carla_data):
    """Detects continuous deceleration periods based on speed thresholds."""
    switch_indices = carla_data.index[carla_data['Mode_Switched'].eq("Yes")]
    temp_periods = []
    for index in switch_indices:
        subset = carla_data.loc[index:].reset_index(drop=True)
        speed_less_than_75 = subset['Lead_Vehicle_Speed'] < 75
        in_deceleration = False
        start_time = None
        
        for i, (time, speed, is_below_threshold) in enumerate(zip(subset['timestamp'], subset['Lead_Vehicle_Speed'], speed_less_than_75)):
            if is_below_threshold and not in_deceleration:
                in_deceleration = True
                start_time = time
            elif not is_below_threshold and in_deceleration:
                in_deceleration = False
                if start_time:
                    end_time = subset['timestamp'][i-1] + 1  
                    temp_periods.append((start_time, end_time))
        
        if in_deceleration and start_time:
            end_time = subset['timestamp'].iloc[-1] + 1
            temp_periods.append((start_time, end_time))

    deceleration_periods = []
    if temp_periods:
        merged_periods = [temp_periods[0]]
        for start, end in temp_periods[1:]:
            last_end = merged_periods[-1][1]
            if start - last_end <= 0.5:
                merged_periods[-1] = (merged_periods[-1][0], end)
            else:
                merged_periods.append((start, end))
        deceleration_periods = merged_periods
    
    return deceleration_periods

def calculate_total_time(deceleration_periods):
    """Calculates the total time based on the number of deceleration periods."""
    num_periods = len(deceleration_periods)
    if num_periods == 0:
        return "No deceleration periods detected."
    elif num_periods < 5:
        total_time = deceleration_periods[-1][1] - deceleration_periods[0][0]
        return f"Total time from the first to the last deceleration period ({num_periods} events): {total_time} seconds"
    else:
        total_time = deceleration_periods[4][1] - deceleration_periods[0][0]
        return f"Total time from the first to the fifth deceleration period: {total_time} seconds"

def process_data(file_path):
    """Loads data, processes it, and calculates total deceleration time."""
    data = pd.read_csv(file_path)
    data = fill_missing_values(data)
    deceleration_periods = detect_deceleration_periods(data)
    return calculate_total_time(deceleration_periods)

# Example usage
file_path = 'path_to_your_data.csv'
result = process_data(file_path)
print(result)
