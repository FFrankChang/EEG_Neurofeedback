import pandas as pd

def match_data(event_file_path, eye_data_file_path, output_file_path):
    event_data = pd.read_csv(event_file_path)
    eye_data = pd.read_csv(eye_data_file_path)

    matched_pupil_diameters = []
    
    for event_timestamp in event_data['timestamp']:
        time_diffs = abs(eye_data['timestamp'] - event_timestamp)
        
        closest_index = time_diffs.idxmin()
        
        matched_pupil_diameter = eye_data.loc[closest_index, 'FilteredPupilDiameter']
        

        matched_pupil_diameters.append(matched_pupil_diameter)
    
    event_data['MatchedFilteredPupilDiameter'] = matched_pupil_diameters
    
    event_data.to_csv(output_file_path, index=False)

event_file = r"G:\Exp_V0_data\data\S08\S08_event_time_filter3.csv"
eye_data_file = r"G:\Exp_V0_data\data\S08\S08_EYE_20241023172122.csv"
output = "out.csv"

match_data(event_file, eye_data_file, output)
