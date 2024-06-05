import pandas as pd
import os

# Define the base directory where the folders are located
base_dir = r"D:\gitee\EEG_Neurofeedback\data"  # Adjust this path
subject = 'yyk'
# Initialize a DataFrame to store the results
columns = ["subject_name", "experiment_no", "scenario", "condition"]
for i in range(1, 6):
    columns += [f"Mean Change Rate {i}", f"Variance {i}", f"Coefficient of Variation {i}"]
# Add columns for averages of the metrics
columns += ["Average Mean Change Rate", "Average Variance", "Average Coefficient of Variation"]
results_df = pd.DataFrame(columns=columns)

# Iterate through each directory in the base directory
for folder in os.listdir(base_dir):
    if 'syr' in folder.lower() and ('easy' in folder.lower() or 'hard' in folder.lower()):
        file_path = os.path.join(base_dir, folder, "carla_merged.csv")
        if os.path.exists(file_path):
            # Load the data
            carla_data = pd.read_csv(file_path)

            # Process 'Mode_Switched'
            carla_data['Mode_Switched'] = carla_data['Mode_Switched'].fillna("No")
            switch_indices = carla_data.index[carla_data['Mode_Switched'].eq("Yes")]

            deceleration_periods = []
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

            # Initialize statistics dictionary
            stats = {}

            # Analyze up to 5 deceleration periods
            for idx, (start, end) in enumerate(deceleration_periods[:5], start=1):
                end_extended = end + 3
                deceleration_data = carla_data[(carla_data['timestamp'] >= start) & (carla_data['timestamp'] <= end_extended)]
                steering_angles = deceleration_data['Steering_Angle']
                stats[f"Mean Change Rate {idx}"] = steering_angles.diff().mean() if not steering_angles.empty else 0
                stats[f"Variance {idx}"] = steering_angles.var() if not steering_angles.empty else 0
                stats[f"Coefficient of Variation {idx}"] = steering_angles.std() / steering_angles.mean() if not steering_angles.empty and steering_angles.mean() != 0 else 0

            # Calculate averages for each metric
            stats["Average Mean Change Rate"] = sum(stats[f"Mean Change Rate {i}"] for i in range(1, 6)) / 5
            stats["Average Variance"] = sum(stats[f"Variance {i}"] for i in range(1, 6)) / 5
            stats["Average Coefficient of Variation"] = sum(stats[f"Coefficient of Variation {i}"] for i in range(1, 6)) / 5

            # Extract experiment number, scenario, and condition from folder name
            experiment_no = ''.join([n for n in folder if n.isdigit()])
            scenario = 'easy' if 'easy' in folder.lower() else 'hard'
            condition = 'silence' if 'silence' in folder.lower() else 'feedback'

            # Append results to DataFrame
            row = {
                "subject_name": subject,
                "experiment_no": experiment_no,
                "scenario": scenario,
                "condition": condition,
            }
            row.update(stats)
            results_df = results_df.append(row, ignore_index=True)

# Save results to a new CSV file
results_df.to_csv(f"./data/{subject}_results.csv", index=False)
