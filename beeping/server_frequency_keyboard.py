import winsound
import threading
import keyboard
import time

frequency = 1

def adjust_frequency():
    global frequency
    while True:
        if keyboard.is_pressed('up'):
            frequency += 1
            print(f"当前频率：{frequency}Hz")
            time.sleep(0.1)  
        elif keyboard.is_pressed('down'):
            frequency = max(1, frequency - 1) 
            print(f"当前频率：{frequency}Hz")
            time.sleep(0.1)  

def play_sound():
    global frequency
    while True:
        winsound.Beep(1500, int(1000 / frequency))
        time.sleep(1 / frequency)  

def main():
    print("初始频率：1Hz (每秒1次响声)")
    threading.Thread(target=adjust_frequency, daemon=True).start()
    threading.Thread(target=play_sound, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == '__main__':
    main()
