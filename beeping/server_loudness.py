import pygame
import threading
import socket
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 初始化pygame的混音器模块
pygame.mixer.init()

# 全局变量设置初始音量和音量历史
loudness = 0.1
loudness_history = []

# 函数：调整音量
def adjust_volume(arousal):
    global loudness
    loudness = arousal  # 直接将接收到的arousal值作为音量
    pygame.mixer.music.set_volume(loudness)
    loudness_history.append(loudness)  # 添加当前音量到历史记录中
    print(f"当前音量：{round(loudness, 2)}")

# 函数：绘制音量历史数据的折线图
def plot_loudness():
    fig, ax = plt.subplots()
    max_points = 100

    def update(frame):
        ax.clear()
        if len(loudness_history) > max_points:
            plot_data = loudness_history[-max_points:]
        else:
            plot_data = loudness_history
        ax.plot(plot_data, label='Loudness')
        ax.set_ylim(0, 1)
        ax.set_title("Real-Time Loudness Level")
        ax.set_xlabel("Time")
        ax.set_ylabel("Loudness")
        ax.legend(loc='upper right')

    ani = FuncAnimation(fig, update, interval=100)
    plt.show()

# 函数：接收音量调节数据
def receive_volume_data(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        if message.startswith("arousal:"):
            arousal_value = float(message.split(":")[1])
            adjust_volume(arousal_value)

# 函数：音频播放控制
def control_audio(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode().strip().lower()

        if command == "play":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
                print("音频播放")
            else:
                print("音频已经在播放中")

        elif command == "pause":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                print("音频暂停")
            else:
                print("音频已经暂停")

        elif command == "stop":
            pygame.mixer.music.stop()
            print("音频停止")
            break

# 主函数
def main():
    pygame.mixer.music.load("one_minute_beeps.wav")
    pygame.mixer.music.set_volume(loudness)
    # pygame.mixer.music.play(-1)  

    # 设置两个端口和套接字
    volume_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    volume_sock.bind(('0.0.0.0', 12345))  # 用于音量调节的端口

    control_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_sock.bind(('0.0.0.0', 12346))  # 用于控制播放状态的端口

    # 创建并启动线程
    volume_thread = threading.Thread(target=receive_volume_data, args=(volume_sock,), daemon=True)
    volume_thread.start()

    control_thread = threading.Thread(target=control_audio, args=(control_sock,), daemon=True)
    control_thread.start()

    plot_thread = threading.Thread(target=plot_loudness, daemon=True)
    plot_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已停止")
        pygame.mixer.quit()
        volume_sock.close()
        control_sock.close()

if __name__ == '__main__':
    main()
