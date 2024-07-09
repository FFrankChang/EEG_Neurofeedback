import socket
import subprocess
import datetime
import csv
import time

# 设置UDP服务器
UDP_IP = "127.0.0.1"  # 本地IP
UDP_PORT = 5005       # 选择一个端口号
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

process = None

# 脚本字典配置，这里可以自由配置路径
scripts = {
    "1": r"D:\carla\carla\PythonAPI\examples\manual_control_steeringwheel_traffic.py",
    "2": "E:\\Carla_Neurofeedback\\s01_main.py",
    "3": "E:\\Carla_Neurofeedback\\s02_main.py"
}

# 记录脚本事件的CSV文件
csv_file_path = 's01_script_events.csv'
# 运行脚本1的持续时间（秒）
RUN_TIME = 600  # 10分钟

try:
    while True:
        data, addr = sock.recvfrom(1024)  # 缓冲区大小是1024字节
        command = data.decode()
        print(f"Received command: {command}")

        if command in ["1", "2", "3"]:
            script_path = scripts[command]
            if process is None:  # 检查是否已经运行一个进程
                process = subprocess.Popen(["python", script_path])
                start_time = time.time()
                print(f"Started script {script_path}.")

                # 如果是脚本1，记录开启时间并设置定时器
                if command == "1":
                    with open(csv_file_path, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(['start_script_1', datetime.datetime.now()])

                    # 等待10分钟后自动关闭脚本1
                    time.sleep(RUN_TIME)
                    process.terminate()
                    print("Automatically terminated script 1 after 10 minutes.")
                    process = None

                    with open(csv_file_path, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(['stop_script_1', datetime.datetime.now()])

                    elapsed_time = time.time() - start_time
                    print(f"Script 1 ran for {elapsed_time:.2f} seconds.")
            else:
                print("Another script is already running.")
        elif command == "0":
            if process is not None:
                process.terminate()  # 终止进程
                print("Terminated the script.")
                if process.args[1] == scripts["1"]:
                    # 如果终止的是脚本1，记录关闭时间
                    with open(csv_file_path, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(['stop_script_1', datetime.datetime.now()])
                process = None
            else:
                print("No script is running.")
finally:
    sock.close()