import pandas as pd

def calculate_arousal_average(csv_file):
    data = pd.read_csv(csv_file)
    
    arousal_average = data['arousal'].mean()
    
    return arousal_average

csv_file_path = 'D:\Frank_Project\EEG_Neurofeedback\data\psd_20240430_145454_pre.csv'

average_arousal = calculate_arousal_average(csv_file_path)
print("Average arousal value:", average_arousal)
