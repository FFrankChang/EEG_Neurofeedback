import pygame
import threading
import keyboard
import time

pygame.mixer.init()

loudness = 0.5

def adjust_volume():
    global loudness
    while True:
        if keyboard.is_pressed('up'):
            loudness = min(1.0, loudness + 0.05)
            pygame.mixer.music.set_volume(loudness)
            print(f"当前音量：{loudness}")
            time.sleep(0.1)  # 增加这个延迟以避免过快调整音量
        elif keyboard.is_pressed('down'):
            loudness = max(0.0, loudness - 0.05)
            pygame.mixer.music.set_volume(loudness)
            print(f"当前音量：{round(loudness,2)}")
            time.sleep(0.1)

def play_audio():
    pygame.mixer.music.load("one_minute_beeps.wav")
    pygame.mixer.music.set_volume(loudness)
    pygame.mixer.music.play(-1)  # 循环播放

    while pygame.mixer.music.get_busy():
        time.sleep(1)

def main():
    print(f"初始音量：{loudness}")

    volume_thread = threading.Thread(target=adjust_volume, daemon=True)
    volume_thread.start()

    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已停止")
        pygame.mixer.quit()

if __name__ == '__main__':
    main()
