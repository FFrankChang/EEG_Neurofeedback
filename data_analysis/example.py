import os
import time
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from data_manager import DataManager
from data_visualizer import DataVisualizer
from data_videoviewer import VideoDataViewer

test_data_folder = '20240425_01'  
data_dir = os.path.join(base_dir, '..', 'data', test_data_folder)

eye_data_path = os.path.join(data_dir, '1eye_test.csv')
carla_data_path = os.path.join(data_dir, '1carla_test.csv')
arousal_data_path = os.path.join(data_dir, '1arousal_test.csv')
raw_data_path = os.path.join(data_dir, '1raw_test.csv')
video_path = os.path.join(data_dir, 'test_video.mp4')
video_start_time = "2024-04-25 17:07:55.368227"

dm = DataManager(eye_data_path, carla_data_path, arousal_data_path, raw_data_path)

# dv = DataVisualizer(dm)
# dv.visualize(['arousal', 'carla', 'eye', 'heart'])

app = VideoDataViewer(video_path, dm, video_start_time, ['arousal','heart'])
app.mainloop()
