import pandas as pd

def load_and_process_data(file_path):
    data = pd.read_csv(file_path)

    subject_scenario_counts = data.groupby(['Subject', 'Scenario']).size().unstack(fill_value=0)

    hard_conditions = data[data['Scenario'] == 'hard'].groupby(['Subject', 'Condition']).size().unstack(fill_value=0)

    easy_conditions = data[data['Scenario'] == 'easy'].groupby(['Subject', 'Condition']).size().unstack(fill_value=0)

    combined_counts = subject_scenario_counts.join(hard_conditions, on='Subject', rsuffix='_hard')
    combined_counts = combined_counts.join(easy_conditions, on='Subject', rsuffix='_easy')

    combined_counts['Trials'] = combined_counts['easy'] + combined_counts['hard']

    cols = combined_counts.columns.tolist()
    cols = cols[-1:] + cols[:-1]  
    combined_counts = combined_counts[cols]

    combined_counts.columns = ['Trials', 'Easy', 'Hard', 'Hard - Feedback', 'Hard - Silence', 'Easy - Feedback', 'Easy - Silence']
    combined_counts.fillna(0, inplace=True)
    combined_counts = combined_counts.astype(int)

    return combined_counts

# Example usage:
file_path = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trails_index.csv'
final_table = load_and_process_data(file_path)
final_table.to_csv('result.csv')
print(final_table)
