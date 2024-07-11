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
base_arousal = 0.0  # Threshold for the minimum arousal value to play sound
loudness = 0
base_volume = 0.05
arousal_history = []  # History of raw arousal values
loudness_history = []
smoothed_loudness_history = []  # History of smoothed loudness values
sound_enabled = True  # Control flag to enable or disable sound

# Function to adjust volume based on smoothed loudness
def adjust_volume(arousal):
    global loudness, sound_enabled
    if not sound_enabled:
        pygame.mixer.music.set_volume(0)
        print("声音已被禁用")
        return

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
    pygame.mixer.music.set_volume(smoothed_loudness + base_volume)
    print(f"当前音量：{round(smoothed_loudness, 2)}")

# Function to control sound based on specific messages
def control_sound(sock):
    global sound_enabled
    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode().strip().lower()

        if command == "silence":
            sound_enabled = False
            pygame.mixer.music.set_volume(0)
            print("音频已静音")
        elif command == "feedback":
            sound_enabled = True
            print("音频已恢复")
        elif command == "stop":
            pygame.mixer.music.stop()
            print("音频停止")

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
def receive_volume_data(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        if message.startswith("arousal:"):
            arousal_value = float(message.split(":")[1])
            adjust_volume(arousal_value)

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

        elif command == "stop":
            pygame.mixer.music.stop()
            print("音频停止")
            break

def pause_audio(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode().strip().lower()

        if command == "pause":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                print("音频暂停")
            else:
                print("音频已经暂停")


# Main function
def main():
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(loudness + base_volume)

    # Set up ports and sockets
    volume_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    volume_sock.bind(('0.0.0.0', 12345))  # Port for volume adjustment

    control_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_sock.bind(('0.0.0.0', 12346))  # Port for playback control

    pause_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pause_sock.bind(('0.0.0.0', 12347))  # Port for pause control

    sound_control_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sound_control_sock.bind(('0.0.0.0', 12348))  # Port for sound control

    # Create and start threads
    volume_thread = threading.Thread(target=receive_volume_data, args=(volume_sock,), daemon=True)
    volume_thread.start()

    control_thread = threading.Thread(target=control_audio, args=(control_sock,), daemon=True)
    control_thread.start()

    pause_thread = threading.Thread(target=pause_audio, args=(pause_sock,), daemon=True)
    pause_thread.start()

    sound_control_thread = threading.Thread(target=control_sound, args=(sound_control_sock,), daemon=True)
    sound_control_thread.start()

    plot_thread = threading.Thread(target=plot_arousal, daemon=True)
    plot_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pygame.mixer.quit()
        volume_sock.close()
        control_sock.close()
        pause_sock.close()
        sound_control_sock.close()

if __name__ == '__main__':
    main()
