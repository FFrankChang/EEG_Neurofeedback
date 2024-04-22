import pygame
import threading
import socket
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 初始化pygame的混音器模块
pygame.mixer.init()

# 设置初始音量
loudness = 0.5
loudness_history = []

# 函数：调整音量
def adjust_volume(arousal):
    global loudness
    loudness = arousal  # 直接将接收到的arousal值作为音量
    pygame.mixer.music.set_volume(loudness)
    loudness_history.append(loudness)  # 添加当前音量到历史记录中
    print(f"当前音量：{round(loudness, 2)}")

# 函数：播放音频
def play_audio():
    pygame.mixer.music.load("one_minute_beeps.wav")
    pygame.mixer.music.set_volume(loudness)
    pygame.mixer.music.play(-1)  # 循环播放

    while pygame.mixer.music.get_busy():
        time.sleep(1)

# 函数：UDP Socket监听并接收数据
def receive_data():
    udp_ip = "localhost"
    udp_port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    while True:
        data, addr = sock.recvfrom(1024)  # 缓冲区大小为1024字节
        message = data.decode()
        if message.startswith("arousal:"):
            arousal_value = float(message.split(":")[1])
            adjust_volume(arousal_value)

def plot_loudness():
    fig, ax = plt.subplots()
    max_points = 20  # 设置滚动窗口大小

    def update(frame):
        ax.clear()
        # 如果数据点数量超过max_points，则只绘制最后的max_points个点
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


def main():
    print(f"初始音量：{loudness}")

    # 创建并启动音频播放线程
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    # 创建并启动数据接收线程
    data_thread = threading.Thread(target=receive_data, daemon=True)
    data_thread.start()

    # 创建并启动绘图线程
    plot_thread = threading.Thread(target=plot_loudness, daemon=True)
    plot_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已停止")
        pygame.mixer.quit()

if __name__ == '__main__':
    main()
