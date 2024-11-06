import os

def batch_rename_csv_files(folder_path):
    count = 0
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".csv") and "EEG" in filename:
                    old_file_path = os.path.join(subfolder_path, filename)
                    new_filename = f"{subfolder}_{filename}"
                    new_file_path = os.path.join(subfolder_path, new_filename)
                    
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} -> {new_file_path}")
                    count+=1
    print('file_count = ',count)
# 设置文件夹A的路径
folder_path = r'G:\Exp_V0_data\data'  
batch_rename_csv_files(folder_path)
