import socket
import keyboard
import time

# 服务器的IP地址和端口号
server_ip = '192.168.3.9'
server_port = 12345

# 初始音量
volume = 0.5

def send_volume(sock, vol):
    # 将音量转换为字符串，并发送到UDP
    message = str(vol).encode()
    sock.sendto(message, (server_ip, server_port))
    print(f"发送音量: {vol}")

def main():
    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        print(f"初始音量：{volume}")
        send_volume(sock, volume)

        while True:
            # 检测向上键是否被按下
            if keyboard.is_pressed('up'):
                volume = min(1.0, volume + 0.05)
                send_volume(sock, volume)
                time.sleep(0.1)  # 避免过快发送数据

            # 检测向下键是否被按下
            elif keyboard.is_pressed('down'):
                volume = max(0.0, volume - 0.05)
                send_volume(sock, volume)
                time.sleep(0.1)  # 避免过快发送数据

            time.sleep(0.05)  # 减少CPU使用率

    except KeyboardInterrupt:
        print("程序已停止")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
