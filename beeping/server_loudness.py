import os
import pygame
import threading
import socket
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize pygame mixer module
pygame.mixer.init()

current_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(current_dir, "heartbeat.mp3")
tor_audio_file = os.path.join(current_dir, "TOR.mp3")

# Global variables for volume settings and history
base_arousal = 0.0 # Threshold for the minimum arousal value to play sound
loudness = 0
base_volume = 0.05
arousal_history = []  # History of raw arousal values
loudness_history = []
smoothed_loudness_history = []  # History of smoothed loudness values

feedback_active = False  # Flag to control feedback activation

# Function to adjust volume based on smoothed loudness
def adjust_volume(arousal):
    global loudness
    arousal_history.append(arousal)  # Append current arousal to history

    if arousal < base_arousal:
        loudness = 0  # Set volume to 0 if arousal is below the threshold
    elif arousal > 1:
        loudness = 1  # Set volume to max if arousal is greater than 1
    else:
        loudness = arousal - base_arousal  # Adjust volume based on arousal

    loudness_history.append(loudness)
    # Compute the average loudness over the last 5 seconds (assuming a frequency of data receipt)
    window_size = 5  # seconds
    if len(loudness_history) > window_size:
        smoothed_loudness = sum(loudness_history[-window_size:]) / window_size
    else:
        smoothed_loudness = sum(loudness_history) / len(loudness_history)

    smoothed_loudness_history.append(smoothed_loudness)
    if feedback_active:
        pygame.mixer.music.set_volume(smoothed_loudness + base_volume)
    else:
        pygame.mixer.music.set_volume(0)
    print(f"当前音量：{round(smoothed_loudness, 2)}")

# Function to plot arousal history graph
def plot_arousal():
    fig, ax = plt.subplots()
    max_points = 100

    def update(frame):
        ax.clear()
        if len(arousal_history) > max_points:
            plot_data = arousal_history[-max_points:]
        else:
            plot_data = arousal_history
        ax.plot(plot_data, label='Arousal')
        ax.set_title("Real-Time Arousal Level")
        ax.set_xlabel("Time")
        ax.set_ylabel("Arousal")
        ax.legend(loc='upper right')

    ani = FuncAnimation(fig, update, interval=100)
    plt.show()

# Function to receive volume adjustment data
def receive_volume_data(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        if message.startswith("arousal:"):
            arousal_value = float(message.split(":")[1])
            adjust_volume(arousal_value)

# Function to control audio playback
def control_audio(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode().strip().lower()

        if command == "play":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            else:
                print("音频已经在播放中")
                
        elif command == "tor":
            tor_channel = pygame.mixer.Channel(1)
            tor_sound = pygame.mixer.Sound(tor_audio_file)
            tor_channel.play(tor_sound)
            print("接管提示")
            
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

# Main function
def main():
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(loudness+base_volume)
    
    global feedback_active
    feedback_mode = input("Enter feedback mode (0 for no feedback, 1 for feedback): ")
    feedback_active = feedback_mode == "1"

    # Set up two ports and sockets
    volume_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    volume_sock.bind(('0.0.0.0', 12345))  # Port for volume adjustment

    control_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_sock.bind(('0.0.0.0', 12346))  # Port for playback control

    # Create and start threads
    volume_thread = threading.Thread(target=receive_volume_data, args=(volume_sock,), daemon=True)
    volume_thread.start()

    control_thread = threading.Thread(target=control_audio, args=(control_sock,), daemon=True)
    control_thread.start()

    plot_thread = threading.Thread(target=plot_arousal, daemon=True)
    plot_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pygame.mixer.quit()
        volume_sock.close()
        control_sock.close()

if __name__ == '__main__':
    main()
