import socket
import keyboard

# Set UDP target IP and port
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Press '0', '1', '2', or '3' to send corresponding number. Press 'esc' to exit.")

try:
    while True:
        # Listen for keyboard events
        if keyboard.is_pressed('1'):
            sock.sendto(b'1', (UDP_IP, UDP_PORT))
            print("Sent '1'")
            while keyboard.is_pressed('1'):
                pass  # Wait for key release to avoid repeated sending
        elif keyboard.is_pressed('0'):
            sock.sendto(b'0', (UDP_IP, UDP_PORT))
            print("Sent '0'")
            while keyboard.is_pressed('0'):
                pass
        elif keyboard.is_pressed('2'):
            sock.sendto(b'2', (UDP_IP, UDP_PORT))
            print("Sent '2'")
            while keyboard.is_pressed('2'):
                pass
        elif keyboard.is_pressed('3'):
            sock.sendto(b'3', (UDP_IP, UDP_PORT))
            print("Sent '3'")
            while keyboard.is_pressed('3'):
                pass
        elif keyboard.is_pressed('esc'):  # Press 'esc' to exit
            print("Exiting.")
            break
finally:
    sock.close()
