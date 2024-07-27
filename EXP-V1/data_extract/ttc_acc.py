import pandas as pd
import numpy as np

def split_steer_column(data):
    """拆分Steer列到三个新列：Steering_Angle, Throttle, Brake"""
    data['Steer'] = data['Steer'].apply(lambda x: eval(x))
    data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0])
    data['Throttle'] = data['Steer'].apply(lambda x: x[1])
    data['Brake'] = data['Steer'].apply(lambda x: x[2])
    data.drop('Steer', axis=1, inplace=True)
    return data

def calculate_ttc(data):
    """计算TTC并更新data"""
    data['Distance'] = np.sqrt((data['Location_x'] - data['Lead_Vehicle_X'])**2 +
                               (data['Location_y'] - data['Lead_Vehicle_Y'])**2 +
                               (data['Location_z'] - data['Lead_Vehicle_Z'])**2)
    data['Relative_Speed'] = abs(data['Speed'] - data['Lead_Vehicle_Speed'])
    data['TTC'] = data['Distance'] / data['Relative_Speed'].replace(0, np.inf)
    return data

def main():
    # Load the CSV file
    file_path = 'path_to_your_csv_file.csv'  # Update the path to your CSV file
    data = pd.read_csv(file_path)
    
    # Process the data
    data = split_steer_column(data)
    data = calculate_ttc(data)
    
    # Find the index of the first 'Yes' in the TOR column
    first_yes_index = data[data['TOR'] == 'Yes'].index[0]
    
    # Extract all data from the first 'Yes' in TOR onwards
    data_post_tor_yes = data.loc[first_yes_index:]
    
    # Calculate the minimum TTC from that data
    min_ttc = data_post_tor_yes['TTC'].min()
    
    # Calculate the standard deviation of Steering_Angle from that data
    steering_angle_std = data_post_tor_yes['Steering_Angle'].std()
    
    # Calculate the average and standard deviation of Acceleration_x from that data
    acceleration_x_mean = data_post_tor_yes['Acceleration_x'].mean()
    acceleration_x_std = data_post_tor_yes['Acceleration_x'].std()
    
    # Calculate the rate of change of Acceleration_x and its mean
    data_post_tor_yes['Acceleration_x_change_rate'] = data_post_tor_yes['Acceleration_x'].diff() / data_post_tor_yes['timestamp'].diff()
    acceleration_x_change_rate_mean = data_post_tor_yes['Acceleration_x_change_rate'].mean()
    
    print(f"The minimum TTC from the first 'Yes' in TOR onwards is: {min_ttc}")
    print(f"The standard deviation of Steering Angle after the first 'Yes' in TOR is: {steering_angle_std}")
    print(f"The average of Acceleration_x after the first 'Yes' in TOR is: {acceleration_x_mean}")
    print(f"The standard deviation of Acceleration_x after the first 'Yes' in TOR is: {acceleration_x_std}")
    print(f"The mean rate of change of Acceleration_x after the first 'Yes' in TOR is: {acceleration_x_change_rate_mean}")

    return data_post_tor_yes

if __name__ == "__main__":
    resulting_data = main()
    # You can do further processing with resulting_data as needed
