import pandas as pd
import os

def find_closest_timestamp(data_df, event_df):
    sample_rate = 1000
    results = []
    for index, event in event_df.iterrows():
        timestamp = event['timestamp']
        # Find the closest timestamp
        closest_idx = (data_df['timestamp'] - timestamp).abs().idxmin()
        # Ensure the first occurrence of duplicate timestamps
        closest_timestamp = data_df.loc[closest_idx, 'timestamp']
        first_occurrence_idx = data_df[data_df['timestamp'] == closest_timestamp].index[0]
        results.append({
            'Latency': first_occurrence_idx / sample_rate,
            'Type': event['Event_Type'],
            'Position': 1
        })
    return results

def process_files(subject, scenario, condition):
    # Load data
    data_df = pd.read_csv(f'{subject}_{scenario}_{condition}.csv')
    event_file_path = f'{subject}_{scenario}_{condition}_event.csv'
    event_df = pd.read_csv(event_file_path)

    # Find the closest timestamp
    results = find_closest_timestamp(data_df, event_df)

    # Save results
    results_df = pd.DataFrame(results)
    results_file_path = f'{subject}_{scenario}_{condition}_event.txt'
    results_df.to_csv(results_file_path, index=False, header=True, sep='\t')

    # Delete the event CSV file
    os.remove(event_file_path) 

def main():
    for i in range(2,8):
        subject = 's' + str(i).zfill(2)
        scenarios = ['easy', 'hard']
        conditions = ['silence', 'feedback']

        for scenario in scenarios:
            for condition in conditions:
                process_files(subject, scenario, condition)

if __name__ == "__main__":
    main()
