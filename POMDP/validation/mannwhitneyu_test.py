import pandas as pd
from scipy.stats import mannwhitneyu
duration = 60

# Load the dataset
file_path = rf'D:\gitee\EEG_Neurofeedback\POMDP\results\final_results_{duration}s.csv'
data = pd.read_csv(file_path)

# Filter data for 'feedback' condition
feedback_data = data[data['Condition'] == 'feedback']

# Specify the columns for Mann-Whitney Test
columns_to_test = ['Min_TTC', 'Steering_Angle_STD', 'Acceleration_x_Mean', 'Acceleration_x_STD', 
                   'Acceleration_x_Change_Rate_Mean', 'Road_Exits']

# Prepare to collect test results
results = []

# Iterate over each specified column
for col in columns_to_test:
    # Create a dictionary to store the selected values for each unique day
    day_groups = {day: group[col].head(5) for day, group in feedback_data.groupby('Day')}
    
    # Check if both days have enough data to perform the test
    if all(len(values) == 5 for values in day_groups.values()):
        # Perform the Mann-Whitney U Test
        u_statistic, p_value = mannwhitneyu(day_groups['D01'], day_groups['D02'])
        
        # Collect the results
        results.append({
            'Column': col,
            'Mann-Whitney_Statistic': u_statistic,
            'P_Value': p_value
        })
    else:
        # Handle the case where there is insufficient data
        results.append({
            'Column': col,
            'Mann-Whitney_Statistic': 'N/A',
            'P_Value': 'Insufficient data'
        })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to a new CSV file
results_path = f'mannwhitney_test_results_{duration}.csv'
results_df.to_csv(results_path, index=False)

print("Tests completed and results saved to:", results_path)
