import pandas as pd
from scipy.stats import mannwhitneyu
import os

# Specify the directory containing the CSV files
directory_path = r'D:\gitee\EEG_Neurofeedback\TRB\data_results'

# List of variables to test
variables = [
    'Min_TTC', 'Steering_Angle_STD', 'Acceleration_x_Mean',
    'Acceleration_x_STD', 'Acceleration_x_Change_Rate_Mean', 'Road_Exits',
    'Average_Lanes_Per_Change', 'Successful_Changes', 'Total_Successful_Change_Time'
]

# List of days to analyze
days = ['D01']

# Initialize an empty DataFrame to store results
results = pd.DataFrame()

# Loop through each CSV file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.csv') and 'wilcoxon' not in filename:
        # Load the data from the CSV file
        file_path = os.path.join(directory_path, filename)
        read_data = pd.read_csv(file_path)

        # Group and aggregate the data
        data = read_data.groupby(['Subject', 'Day', 'Condition', 'Group']).agg({
            'Min_TTC': 'mean',
            'Steering_Angle_STD': 'mean',
            'Acceleration_x_Mean': 'mean',
            'Acceleration_x_STD': 'mean',
            'Acceleration_x_Change_Rate_Mean': 'mean',
            'Road_Exits': 'mean',
            'Average_Lanes_Per_Change': 'mean',
            'Successful_Changes': 'mean',
            'Total_Successful_Change_Time': 'mean'
        }).reset_index()

        # Loop through each day and perform Mann-Whitney U test for each variable
        for day in days:
            filtered_data = data[(data['Condition'] == 'feedback') & (data['Day'] == day)]
            
            for variable in variables:
                group_bci_data = filtered_data[filtered_data['Group'] == 'Real'][variable]
                group_sham_data = filtered_data[filtered_data['Group'] == 'Sham'][variable]
                
                # Handle cases where one or both groups might be empty
                if group_bci_data.empty or group_sham_data.empty:
                    u_stat, p_value = None, None  # Assign None if data is insufficient
                    significant = 'No Data'  # Indicate no data available for testing
                else:
                    u_stat, p_value = mannwhitneyu(group_bci_data, group_sham_data, alternative='two-sided')
                    significant = 'Yes' if p_value < 0.05 else 'No'
                
                # Append results with filename included
                results = results.append({
                    'Day': day,
                    'Variable': variable,
                    'U_Statistic': u_stat,
                    'P_Value': p_value,
                    'Significant': significant,
                    'Filename': filename
                }, ignore_index=True)

# Save results to a new CSV
results_file_path = 'mmm.csv'
results.to_csv(results_file_path, index=False)

print(f"Results saved to {results_file_path}")
