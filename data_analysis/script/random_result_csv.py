import pandas as pd

# Load the data from the CSV file
file_path = r'D:\gitee\EEG_Neurofeedback\all_results.csv'  # Adjust the path to where your CSV file is located
data = pd.read_csv(file_path)

# Filter data for 'hard' condition
hard_data = data[data['scenario'] == 'hard']
print(hard_data)
# Prepare the result dataframe
result_df = pd.DataFrame(columns=['subject_name', 'silence_avg_coef_var', 'feedback_avg_coef_var'])

# Process data for each subject
for subject in hard_data['subject_name'].unique():
    # Randomly select one 'silence' and one 'feedback' data point for the subject
    subject_data = hard_data[hard_data['subject_name'] == subject]
    silence_sample = subject_data[subject_data['condition'] == 'silence'].sample(n=1)
    feedback_sample = subject_data[subject_data['condition'] == 'feedback'].sample(n=1)
    
    # Calculate the average coefficient of variation for silence and feedback
    silence_avg_coef_var = silence_sample['Average Coefficient of Variation'].values[0]
    feedback_avg_coef_var = feedback_sample['Average Coefficient of Variation'].values[0]
    
    # Append results to the dataframe
    result_df = result_df.append({
        'subject_name': subject,
        'silence_avg_coef_var': silence_avg_coef_var,
        'feedback_avg_coef_var': feedback_avg_coef_var
    }, ignore_index=True)

# Save the result to a new CSV file
output_file_path = r'aa.csv'
result_df.to_csv(output_file_path, index=False)
