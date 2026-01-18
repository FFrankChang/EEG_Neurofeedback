import os
import pygame
import threading
import socket
import time
import random
from collections import deque

# Initialize pygame mixer module
pygame.mixer.init()

current_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(current_dir, "heartbeat_5s.mp3")

# Global state variables
current_mode = "silence"  # feedback, silence, stop, RL
mode_lock = threading.Lock()
volume_lock = threading.Lock()

# Volume control with sliding window
volume_history = deque(maxlen=10)  # 滑窗大小为10，避免音量波动太快
current_volume = 0.5
base_volume = 0.05
max_volume = 1
min_volume = 0.1

# RL mode control variables
rl_playing = False
rl_last_play_time = 0
rl_play_duration = 5  # Will be randomly set to 5 or 10
rl_pause_duration = 15  # Pause duration between RL plays (longer interval)

# Feedback mode control
feedback_playing = False

def get_random_volume():
    """Generate random volume with some variance"""
    return random.uniform(min_volume, max_volume)

def update_volume_smooth():
    """Update volume with sliding window smoothing"""
    global current_volume
    
    with volume_lock:
        # Generate new random volume
        new_volume = get_random_volume()
        volume_history.append(new_volume)
        
        # Calculate smoothed volume using sliding window
        if len(volume_history) > 0:
            current_volume = sum(volume_history) / len(volume_history)
        else:
            current_volume = new_volume
        
        # Set the volume in pygame
        pygame.mixer.music.set_volume(current_volume + base_volume)
        
    return current_volume

def play_audio_continuously():
    """Thread function for feedback mode - continuous audio playback"""
    global feedback_playing
    
    while True:
        with mode_lock:
            mode = current_mode
        
        if mode == "feedback":
            if not feedback_playing:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                feedback_playing = True
                print(f"[Feedback] 开始持续播放音频，音量: {current_volume:.2f}")
            
            # Update volume randomly with smoothing
            vol = update_volume_smooth()
            time.sleep(1)  # Update volume every second
            print(f"[Feedback] 当前音量: {vol:.2f}")
        else:
            if feedback_playing:
                pygame.mixer.music.stop()
                feedback_playing = False
                print("[Feedback] 停止播放")
            time.sleep(0.1)

def play_audio_rl():
    """Thread function for RL mode - intermittent audio playback"""
    global rl_playing, rl_last_play_time, rl_play_duration
    
    while True:
        with mode_lock:
            mode = current_mode
        
        if mode == "RL":
            current_time = time.time()
            
            # Check if it's time to play
            if not rl_playing and (current_time - rl_last_play_time >= rl_pause_duration):
                # Randomly choose play duration: 5s or 10s
                rl_play_duration = random.choice([5, 10])
                
                # Load and play audio
                pygame.mixer.music.load(audio_file)
                vol = update_volume_smooth()
                pygame.mixer.music.play()
                rl_playing = True
                rl_last_play_time = current_time
                print(f"[RL] 开始播放 {rl_play_duration}秒，音量: {vol:.2f}")
                
                # Play for the determined duration
                time.sleep(rl_play_duration)
                
                # Stop playing
                pygame.mixer.music.stop()
                rl_playing = False
                print(f"[RL] 停止播放，等待 {rl_pause_duration}秒后再次播放")
            else:
                # Wait a bit before checking again
                time.sleep(0.5)
        else:
            if rl_playing:
                pygame.mixer.music.stop()
                rl_playing = False
                print("[RL] 停止播放")
            time.sleep(0.1)

def handle_command(command):
    """Handle incoming commands"""
    global current_mode, rl_last_play_time
    
    command = command.strip().lower()
    
    with mode_lock:
        old_mode = current_mode
        
        if command == "feedback":
            current_mode = "feedback"
            print(f"[命令] 切换到 Feedback 模式 (持续播放)")
        elif command == "silence":
            current_mode = "silence"
            pygame.mixer.music.stop()
            print(f"[命令] 切换到 Silence 模式 (静音)")
        elif command == "stop":
            pygame.mixer.music.stop()
            print(f"[命令] 停止播放当前音频")
            # Don't change mode, just stop current playback
            return
        elif command == "rl":
            current_mode = "RL"
            rl_last_play_time = 0  # Reset timer to allow immediate play
            print(f"[命令] 切换到 RL 模式 (间歇性播放)")
        else:
            print(f"[命令] 未知命令: {command}")
            return
        
        if old_mode != current_mode:
            print(f"[模式切换] {old_mode} -> {current_mode}")

def receive_commands(sock):
    """Thread function to receive control commands via UDP"""
    print("[UDP] 等待接收命令...")
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            command = data.decode()
            print(f"[接收] 来自 {addr} 的命令: {command}")
            handle_command(command)
        except Exception as e:
            print(f"[错误] 接收命令时出错: {e}")

def main():
    print("=" * 50)
    print("音频控制服务器 v4")
    print("=" * 50)
    print("命令列表:")
    print("  - feedback: 持续播放音频")
    print("  - silence: 静音模式")
    print("  - stop: 停止当前播放")
    print("  - RL: 间歇性播放 (5s或10s，随机)")
    print("=" * 50)
    
    # Set up socket for receiving commands
    command_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_sock.bind(('0.0.0.0', 12348))  # Port for receiving commands
    print(f"[UDP] 监听端口 12348")
    
    # Create and start threads
    command_thread = threading.Thread(target=receive_commands, args=(command_sock,), daemon=True)
    command_thread.start()
    
    feedback_thread = threading.Thread(target=play_audio_continuously, daemon=True)
    feedback_thread.start()
    
    rl_thread = threading.Thread(target=play_audio_rl, daemon=True)
    rl_thread.start()
    
    try:
        print("[主线程] 服务器运行中，按 Ctrl+C 退出...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[退出] 正在关闭服务器...")
        pygame.mixer.quit()
        command_sock.close()
        print("[退出] 服务器已关闭")

if __name__ == '__main__':
    main()
