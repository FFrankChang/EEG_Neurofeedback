import os

# Mapping of current directory names ('Name') to new directory names ('Subject No')
name_to_subject = {
    "syr": "S01",
    "lba": "S02",
    "syh": "S03",
    "llk": "S04",
    "lr": "S05",
    "krx": "S06",
    "wj": "S07",
    "lxk": "S08",
    "yh": "S09",
    "sby": "S10"
}

# Specify the path to the directory containing the folders to be renamed
path_to_directories = r'F:\NFB_EXP\Exp_V1_data\filtered'

def rename_directories_and_files(root_directory):
    for root, dirs, files in os.walk(root_directory):
        # Rename directories if needed
        for dir_name in dirs:
            name_part = dir_name.split('_')[0]
            if name_part in name_to_subject:
                new_directory_name = dir_name.replace(name_part, name_to_subject[name_part])
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, new_directory_name)
                os.rename(old_path, new_path)
                print(f"Renamed directory {old_path} to {new_path}")

        # Rename CSV files containing 'carla'
        for file_name in files:
            if file_name.endswith('.csv') and 'carla' in file_name:
                name_part = file_name.split('_')[2]
                if name_part in name_to_subject:
                    new_file_name = file_name.replace(name_part, name_to_subject[name_part])
                    old_file_path = os.path.join(root, file_name)
                    new_file_path = os.path.join(root, new_file_name)
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed file {old_file_path} to {new_file_path}")

# Start the renaming process
rename_directories_and_files(path_to_directories)
print("All relevant directories and files have been renamed.")
