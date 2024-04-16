import socket
import time
import random

def send_data_b():
    host = 'localhost'
    port = 12346
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            data_b = random.uniform(1, 100)
            print(f"Sending data B: {data_b}")
            sock.sendto(str(data_b).encode(), (host, port))
            time.sleep(4)  
    except KeyboardInterrupt:
        print("Data B sender stopped.")
        sock.close()

if __name__ == '__main__':
    send_data_b()
