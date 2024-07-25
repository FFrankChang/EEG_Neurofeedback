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

import os

# Specify the path to the directory containing the folders to be renamed
path_to_directories = r'F:\NFB_EXP\Exp_V1_data\filtered'

# Loop through the directory names in the specified path
for directory in os.listdir(path_to_directories):
    # Extract the 'Name' part from the directory name
    name_part = directory.split('_')[0]
    # Check if this part is in the mapping
    if name_part in name_to_subject:
        # Generate the new directory name by replacing 'Name' with 'Subject No' and keeping the suffix
        new_directory_name = directory.replace(name_part, name_to_subject[name_part])
        # Generate the full paths for the old and new directory names
        old_path = os.path.join(path_to_directories, directory)
        new_path = os.path.join(path_to_directories, new_directory_name)
        
        # Rename the directory
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

print("All relevant directories have been renamed.")
