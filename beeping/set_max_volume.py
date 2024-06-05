import os
import pygame
import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import time

pygame.mixer.init()
current_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(current_dir, "long_heartbeat.mp3")
sound = pygame.mixer.Sound(audio_path)
sound.set_volume(1) 

# 开始循环播放音频
sound.play(loops=-1)

# 获取默认音频设备
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

def volume_up():
    current_vol = volume.GetMasterVolumeLevel()
    max_vol = volume.GetVolumeRange()[1]
    new_vol = min(max_vol, current_vol + 1.0)
    volume.SetMasterVolumeLevel(new_vol, None)
    print(f"Volume increased to {current_vol:.0f} dB -> {new_vol:.0f} dB")

def volume_down():
    current_vol = volume.GetMasterVolumeLevel()
    min_vol = volume.GetVolumeRange()[0]
    new_vol = max(min_vol, current_vol - 1.0)  
    volume.SetMasterVolumeLevel(new_vol, None)
    print(f"Volume decreased from {current_vol:.0f} dB -> {new_vol:.0f} dB")

keyboard.add_hotkey('up', volume_up)
keyboard.add_hotkey('down', volume_down)

try:
    while True:
        time.sleep(1)  
except KeyboardInterrupt:
    print("Exited by user")
    pygame.mixer.quit()
