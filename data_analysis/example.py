import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

from data_manager import DataManager
from data_visualizer import DataVisualizer

def auto_load_data(data_manager, directory):
    """Automatically load data by identifying files based on naming conventions."""
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

test_data_folder = '20240430_01_final_02'
data_dir = os.path.join(base_dir, '..', 'data', test_data_folder)

dm = DataManager()
auto_load_data(dm, data_dir)

dv = DataVisualizer(dm)

dv.visualize(['arousal', 'carla', 'eye', 'heart'])
