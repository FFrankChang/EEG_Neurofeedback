import winsound
import threading
import socket
import time

frequency = 1

def udp_receiver(port, value_container):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", port))
    while True:
        data, _ = sock.recvfrom(1024)  # buffer size is 1024 bytes
        value_container['value'] = float(data.decode())

def calculate_frequency(a_container, b_container):
    global frequency
    while True:
        try:
            a = a_container['value']
            b = b_container['value']
            if b != 0:
                new_frequency = a / b
                if new_frequency != frequency:
                    frequency = max(1, int(new_frequency))
                    print(f"新的频率：{frequency}Hz")
        except KeyError:
            continue  
        time.sleep(0.1)  

def play_sound():
    global frequency
    while True:
        winsound.Beep(1500, int(1000 / frequency))
        time.sleep(1 / frequency)  

def main():
    a_container = {}
    b_container = {}

    threading.Thread(target=udp_receiver, args=(12345, a_container), daemon=True).start()
    threading.Thread(target=udp_receiver, args=(12346, b_container), daemon=True).start()
    threading.Thread(target=calculate_frequency, args=(a_container, b_container), daemon=True).start()
    threading.Thread(target=play_sound, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == '__main__':
    main()
