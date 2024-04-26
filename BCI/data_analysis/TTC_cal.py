import os
import pandas as pd
import numpy as np

def calculate_ttc(data_path):
    # Load the data from the CSV file
    data = pd.read_csv(data_path)

    # Calculate the Euclidean distance between the main vehicle and the lead vehicle
    data['Distance'] = np.sqrt((data['Location_x'] - data['Lead_Vehicle_X'])**2 +
                               (data['Location_y'] - data['Lead_Vehicle_Y'])**2 +
                               (data['Location_z'] - data['Lead_Vehicle_Z'])**2)

    # Calculate the relative speed (absolute difference in speeds between the main and lead vehicles)
    data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed'])

    # Calculate TTC (Time to Collision)
    data['TTC'] = data['Distance'] / data['Relative_Speed'].replace(0, np.inf)

    # Determine the directory and base name of the original file
    directory, base_filename = os.path.split(data_path)
    new_filename = base_filename.replace('.csv', '_TTC.csv')

    # Save the updated data frame to a new CSV file
    output_file_path = os.path.join(directory, new_filename)
    data.to_csv(output_file_path, index=False)
    return output_file_path

# Example usage:
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(base_path, 'data', 'mainvehicle_20240425170754_1.csv')
updated_file_path = calculate_ttc(data_path)
print("Updated file saved to:", updated_file_path)
