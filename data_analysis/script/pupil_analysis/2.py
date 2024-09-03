import pandas as pd
import json
import socket
import time

# Load the CSV file and remove the timestamp column
file_path = r'C:\Users\001\Downloads\EYE_20240708182416.csv'
data = pd.read_csv(file_path)
data = data.drop(columns=['timestamp'])

# Set up the UDP connection
UDP_IP = "127.0.0.1"
UDP_PORT = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to send data at 60Hz
def send_data():
    for index, row in data.iterrows():
        message = row.to_json()
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        time.sleep(1/60)  # Sleep to maintain 60Hz frequency

if __name__ == "__main__":
    send_data()
