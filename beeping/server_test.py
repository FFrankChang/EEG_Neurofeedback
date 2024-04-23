import random 
import socket
import time

udp_ip = "localhost"
udp_port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    arousal = random.random()
    message = f"arousal:{arousal}"
    sock.sendto(message.encode(), (udp_ip, udp_port))
    time.sleep(1)