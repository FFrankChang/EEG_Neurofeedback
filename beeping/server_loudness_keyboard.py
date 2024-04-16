import pygame
import threading
import keyboard
import time

# 初始化 Pygame 混音器
pygame.mixer.init()

# 设置全局变量控制音量
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
            print(f"当前音量：{loudness}")
            time.sleep(0.1)

def play_audio():
    # 加载音频文件并设置初始音量
    pygame.mixer.music.load("one_minute_beeps.wav")
    pygame.mixer.music.set_volume(loudness)
    pygame.mixer.music.play(-1)  # 循环播放

    # 使音频播放线程持续运行，直到主线程结束
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def main():
    print(f"初始音量：{loudness}")

    # 创建和启动音量调整线程
    volume_thread = threading.Thread(target=adjust_volume, daemon=True)
    volume_thread.start()

    # 创建和启动音频播放线程
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    # 保持主线程运行，直到发生键盘中断
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已停止")
        pygame.mixer.quit()

if __name__ == '__main__':
    main()
