import os
import csv

def count_files_in_folder(folder_path):
    # Dictionary to store the results for this folder
    folder_results = {
        "C01": {"feedback": 0, "silence": 0},
        "C02": {"feedback": 0, "silence": 0}
    }

    # Only list files in the given directory (not recursively)
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.endswith(".csv"):
            # Check for file category and type
            if 'C01' in file:
                if 'feedback' in file:
                    folder_results['C01']['feedback'] += 1
                elif 'silence' in file:
                    folder_results['C01']['silence'] += 1
            elif 'C02' in file:
                if 'feedback' in file:
                    folder_results['C02']['feedback'] += 1
                elif 'silence' in file:
                    folder_results['C02']['silence'] += 1

    return folder_results

def save_results_to_csv(all_results, output_path):
    # Define headers
    headers = ['Folder', 'Category', 'Feedback Count', 'Silence Count']
    
    # Write to CSV
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for folder, results in all_results.items():
            for category, counts in results.items():
                row = [folder, category, counts['feedback'], counts['silence']]
                writer.writerow(row)

def main(directory_path, output_csv_path):
    all_results = {}
    # Walk through all directories in the given directory
    for folder in next(os.walk(directory_path))[1]:
        full_path = os.path.join(directory_path, folder)
        # Collect results for each folder
        folder_results = count_files_in_folder(full_path)
        all_results[folder] = folder_results

    # Save all results to CSV
    # save_results_to_csv(all_results, output_csv_path)

    # Optionally, print the results
    for folder, results in all_results.items():
        print(f"Folder: {folder}")
        for category, counts in results.items():
            print(f"  Category: {category}, Feedback: {counts['feedback']}, Silence: {counts['silence']}")

# Usage example
directory_path = r'E:\NFB_data_backup\20240730'  # Specify the directory path here
output_csv_path = 'output.csv'  # Specify the output CSV file path here
main(directory_path, output_csv_path)
