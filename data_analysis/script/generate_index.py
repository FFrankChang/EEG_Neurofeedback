import os
import csv

def parse_folder_name(folder_name):
    parts = folder_name.split('_')
    if len(parts) != 5:
        return None 
    return {
        'Date': parts[0],
        'Subject': parts[1],
        'ExperimentNo': parts[2],
        'Scenario': parts[3],
        'Condition': parts[4]
    }

def generate_csv(base_path):
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    csv_file_path = os.path.join(base_path, 'trails_index.csv')
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Date', 'Subject', 'ExperimentNo', 'Scenario', 'Condition', 'FolderPath']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for folder in folders:
            folder_info = parse_folder_name(folder)
            if folder_info and 'invalid' not in folder_info['Condition']: 
                folder_info['FolderPath'] = os.path.join(base_path, folder)
                writer.writerow(folder_info)

# 使用示例
base_path = r'D:\gitee\EEG_Neurofeedback\data'
generate_csv(base_path)
