import os
import pandas as pd

def find_problem_csvs(folder):
    problem_files = []
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if 'EYE' in file and file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                try:
                    data = pd.read_csv(file_path)
                    if 'FilteredPupilDiameter' in data.columns:
                        if data['FilteredPupilDiameter'].isnull().all():
                            problem_files.append(file_path)
                    else:
                        problem_files.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return problem_files

folder = 'G:\Exp_V0_data\data'  
problem_csvs = find_problem_csvs(folder)

for f in problem_csvs:
    print(f)
