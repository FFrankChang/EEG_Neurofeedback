import socket
import time
import random
import threading
import keyboard  # Import the keyboard library to detect key presses

def send_data(port, stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while not stop_event.is_set():
            data = random.uniform(0, port-5000)  # Generate random arousal level
            # print(f"Sending {data} to port {port}")
            sock.sendto(str(data).encode(), ('localhost', port))
            time.sleep(0.01)  # Send data every second
        print(f"Stopping thread for port {port}")

def main():
    stop_event = threading.Event()  # Event to signal the threads to stop
    ports = [5001, 5002, 5003]  # List of ports to send data to
    threads = []

    for port in ports:
        thread = threading.Thread(target=send_data, args=(port, stop_event))
        threads.append(thread)
        thread.start()

    # Wait for the ESC key to be pressed
    keyboard.wait('esc')
    stop_event.set()  # Signal all threads to stop

    for thread in threads:
        thread.join()  # Wait for all threads to finish
    print("All threads have been stopped.")

if __name__ == "__main__":
    main()
