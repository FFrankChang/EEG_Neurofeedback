import pygame
import threading
import time
import socket

pygame.mixer.init()

def control_audio(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # 缓冲大小1024字节
        command = data.decode().strip().lower()  # 接收并转化命令为小写

        if command == "play":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  # 未播放时开始循环播放
                print("音频播放")
            else:
                print("音频已经在播放中")

        elif command == "pause":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()  # 暂停播放
                print("音频暂停")
            else:
                print("音频已经暂停")

        elif command in ["stop", "end"]:
            pygame.mixer.music.stop()  # 停止播放
            print("音频停止")
            break  # 退出循环，结束线程

        time.sleep(0.1)  # 延迟以避免过快处理命令

def setup_audio():
    pygame.mixer.music.load("one_minute_beeps.wav")
    pygame.mixer.music.set_volume(0.5)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 12346))  # 监听所有到达12345端口的数据

    setup_audio()  # 配置音频文件和初始音量

    control_thread = threading.Thread(target=control_audio, args=(sock,), daemon=True)
    control_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已停止")
        pygame.mixer.quit()
        sock.close()

if __name__ == '__main__':
    main()
