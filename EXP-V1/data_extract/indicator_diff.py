import pandas as pd

def load_and_prepare_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    return data

def compute_differences(data):
    # Group by Subject and Day, and pivot to make 'Condition' a sublevel in columns
    grouped = data.groupby(['Subject', 'Day', 'Condition']).mean()
    pivot_data = grouped.unstack(level=-1)

    # Calculate the difference metrics: feedback - silence
    difference_metrics = pivot_data.xs('feedback', level='Condition', axis=1) - pivot_data.xs('silence', level='Condition', axis=1)
    return difference_metrics

def evaluate_improvement(difference_metrics):
    # Define which metrics are 'better' when higher or lower
    better_higher = ['Min_TTC', 'Successful_Changes', 'Total_Successful_Change_Time']
    better_lower = ['Steering_Angle_STD', 'Acceleration_x_STD', 'Acceleration_x_Change_Rate_Mean', 'Road_Exits', 'Average_Lanes_Per_Change']

    # Evaluate improvements
    improvement = {}
    for metric in better_higher:
        improvement[metric] = (difference_metrics[metric] > 0).astype(int)  # 1 if feedback is better
    for metric in better_lower:
        improvement[metric] = (difference_metrics[metric] < 0).astype(int)  # 1 if feedback is better
    
    # Convert improvement dictionary into a DataFrame
    improvements_df = pd.DataFrame(improvement)
    return improvements_df

def main():
    # Specify the path to your data file
    file_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\grouped_expv1_c01_results_d.csv'

    # Load and prepare the data
    data = load_and_prepare_data(file_path)
    
    # Compute differences between conditions
    differences = compute_differences(data)
    
    # Evaluate which metrics improved under the feedback condition
    improvements = evaluate_improvement(differences)
    
    # Save the results to a CSV file
    improvements.to_csv('xx.csv')
    
    # Print the results
    print(improvements)

if __name__ == "__main__":
    main()
