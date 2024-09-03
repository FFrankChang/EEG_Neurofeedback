import os

def rename_files(directory):
    
    os.chdir(directory)
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            new_filename = filename.replace("D04", "D02")
            os.rename(filename, new_filename)
            print(f'Renamed "{filename}" to "{new_filename}"')
directory_path = r'E:\NFB_data_backup\nfb_20240820'
rename_files(directory_path)
