import os
import sys
import tkinter as tk
from tkinter import filedialog

base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from data_manager import DataManager
from data_visualizer import DataVisualizer
from data_videoviewer import VideoDataViewer

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

def select_folder():
    root = tk.Tk()
    root.withdraw()
    default_data_dir = os.path.join(base_dir, '..', 'data')
    folder_selected = filedialog.askdirectory(initialdir=default_data_dir)
    root.destroy()
    return folder_selected

data_dir = select_folder()
folder_name = os.path.basename(data_dir)

video_start_time = "2024-05-28 15:20:55.925"

dm = DataManager(data_dir)
video_path = auto_load_data(dm, data_dir)

dv = DataVisualizer(dm)
fig = dv.visualize(['arousal', 'carla', 'eye', 'heart'])
dv.save_figure(fig)
# app = VideoDataViewer(video_path, dm, ['arousal','heart'],start_time=video_start_time,annotation_mode=True)
# app.mainloop()