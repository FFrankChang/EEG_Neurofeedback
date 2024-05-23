import socket
import os
import keyboard

def receive_files(server_ip, server_port, script_dir):
    save_path = os.path.join(script_dir, "data")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    def get_unique_filename(directory, filename):
        base, extension = os.path.splitext(filename)
        counter = 1
        unique_filename = filename
        while os.path.exists(os.path.join(directory, unique_filename)):
            unique_filename = f"{base}({counter}){extension}"
            counter += 1
        return unique_filename

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_ip, server_port))
        s.listen(1)
        print(f"Server listening on {server_ip}:{server_port}...")

        while True:
            if keyboard.is_pressed('esc'):
                print("ESC pressed, exiting...")
                break
            
            s.settimeout(0.5)  
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            
            with conn:
                print(f"Connected by {addr}")
                try:
                    while True:
                        file_size_data = conn.recv(1024)
                        if not file_size_data:
                            break
                        file_size = int(file_size_data.decode())
                        conn.sendall(b"OK")
                        
                        file_name = conn.recv(1024).decode()
                        conn.sendall(b"OK")
                        
                        unique_file_name = get_unique_filename(save_path, file_name)
                        
                        with open(os.path.join(save_path, unique_file_name), 'wb') as f:
                            received = 0
                            while received < file_size:
                                data = conn.recv(4096)
                                if not data:
                                    break
                                f.write(data)
                                received += len(data)
                        print(f"Received file: {unique_file_name}")
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receive_files("0.0.0.0", 7999, script_dir)
