import os
import pandas as pd

def split_steer_column(data):
    # 拆分Steer列为Steering_Angle, Throttle, Brake
    data['Steer'] = data['Steer'].apply(lambda x: eval(x))
    data['Steering_Angle'] = data['Steer'].apply(lambda x: x[0] * 540)
    data['Throttle'] = data['Steer'].apply(lambda x: x[1])
    data['Brake'] = data['Steer'].apply(lambda x: x[2])
    data.drop('Steer', axis=1, inplace=True)
    return data

def process_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        results_path = os.path.join(subdir, 'updated_carla_results.csv')
        if os.path.isfile(results_path):
            results_df = pd.read_csv(results_path)
            for file_name in results_df.iloc[:, 0]:
                if 'C01' in file_name:
                    file_path = os.path.join(subdir, file_name)
                    if os.path.isfile(file_path):
                        data = pd.read_csv(file_path)
                        if 'Steer' in data.columns:
                            data = split_steer_column(data)
                            data.to_csv(file_path, index=False)
                            print(f"Processed and updated {file_path}")
                        else:
                            print(f"'Steer' column not found in {file_path}.")
                    else:
                        print(f"File {file_name} not found in {subdir}.")
                else:
                    print(f"File {file_name} does not contain 'C01' and is not processed.")

root_directory = r'E:\NFB_data_backup\20240730'
process_files(root_directory)
