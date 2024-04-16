import socket
import time
import random

def send_data_a():
    host = 'localhost'
    port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            data_a = random.uniform(1, 100)
            print(f"Sending data A: {data_a}")
            sock.sendto(str(data_a).encode(), (host, port))
            time.sleep(2) 
    except KeyboardInterrupt:
        print("Data A sender stopped.")
        sock.close()

if __name__ == '__main__':
    send_data_a()
