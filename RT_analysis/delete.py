import os
import fnmatch

def delete_filtered_csv(directory, pattern="*filter*.csv"):
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            file_path = os.path.join(root, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

folder_path = r'G:\Exp_V0_data\data'  
delete_filtered_csv(folder_path)
