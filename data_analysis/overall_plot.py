import os
import sys
import tkinter as tk
from tkinter import filedialog
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from data_manager import DataManager
from data_visualizer import DataVisualizer
from data_videoviewer import VideoDataViewer

def filter_folder_paths(csv_file_path, date=None, subject=None, experiment_no=None, scenario=None, condition=None):
    data = pd.read_csv(csv_file_path)
    if date:
        data = data[data['Date'] == date]
    if subject:
        data = data[data['Subject'] == subject]
    if experiment_no:
        data = data[data['ExperimentNo'] == experiment_no]
    if scenario:
        data = data[data['Scenario'] == scenario]
    if condition:
        data = data[data['Condition'] == condition]
    return data['FolderPath'].tolist()

def auto_load_data(data_manager, directory):
    video_path = ''
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if 'Recording' in file:
            data_manager.load_eye_data(file_path)
        elif 'carla_2024' in file:
            data_manager.load_carla_data(file_path)
        elif 'eegraw' in file:
            data_manager.load_ecg_data(file_path)
        elif 'psd' in file:
            data_manager.load_eeg_data(file_path)
        elif file.endswith('.mp4') or file.endswith('.MOV'):
            video_path = file_path
    return video_path

def process_data_folders(csv_file_path,subject):
    folder_paths = filter_folder_paths(csv_file_path,subject=subject)
    for folder in folder_paths:
        dm = DataManager(folder)
        video_path = auto_load_data(dm, folder)

        dv = DataVisualizer(dm)
        fig = dv.visualize(['arousal', 'carla', 'eye', 'heart'],display=False)

        # Save figures in a dedicated folder for each date or experiment
        result_folder = r'D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\overall'
        dv.save_figure(fig, path=result_folder)

csv_file_path = r"D:\gitee\EEG_Neurofeedback\data_analysis\results\20240606\20240606_trials_index.csv"
for i in range(1,11):
    subject = 's' + str(i).zfill(2)
    process_data_folders(csv_file_path,subject)
