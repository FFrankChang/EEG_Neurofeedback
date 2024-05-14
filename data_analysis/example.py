import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from data_manager import DataManager
from data_visualizer import DataVisualizer
from data_videoviewer import VideoDataViewer

def auto_load_data(data_manager, directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if 'Recording' in file:
            data_manager.load_eye_data(file_path)
        elif 'carla' in file:
            data_manager.load_carla_data(file_path)
        elif 'eegraw' in file:
            data_manager.load_ecg_data(file_path)
        elif 'psd' in file:
            data_manager.load_eeg_data(file_path)
        elif file.endswith('.mp4') or file.endswith('.MOV'):
            video_path = file_path
    return video_path

test_data_folder = '20240512_03'
data_dir = os.path.join(base_dir, '..', 'data', test_data_folder)

video_start_time = "2024-04-30 15:27:19.997"

dm = DataManager()
video_path = auto_load_data(dm, data_dir)

# dv = DataVisualizer(dm)
# dv.visualize(['arousal', 'carla', 'eye', 'heart'])

app = VideoDataViewer(video_path, dm, ['arousal','heart'])
app.mainloop()
