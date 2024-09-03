import tkinter as tk
from tkinter import ttk
import socket
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from collections import deque
import cv2
from tkinter import Label
from PIL import Image, ImageTk

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Data Visualization Dashboard')
        self.geometry('1920x1080')

        # Setup UDP Socket
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.date = ''
        self.subject = ''
        
        # Data deques
        self.max_points = 120
        self.times = deque(maxlen=self.max_points)
        self.left_pupil_diameters = deque(maxlen=self.max_points)
        self.right_pupil_diameters = deque(maxlen=self.max_points)
        self.left_eyelid_openings = deque(maxlen=self.max_points)
        self.right_eyelid_openings = deque(maxlen=self.max_points)
        
        # Initialize frames
        self.preparation_frame = tk.Frame(self)
        self.monitoring_frame = tk.Frame(self)
        self.statistics_frame = tk.Frame(self)

        # Setup pages
        self.setup_preparation_page()
        self.setup_monitoring_page()
        self.setup_statistics_page()

    def setup_preparation_page(self):
        self.preparation_frame.pack(fill='both', expand=True)

        # Label and input for participant name
        participant_label = tk.Label(self.preparation_frame, text="Participant Name:")
        participant_label.pack(pady=(10, 5))
        self.participant_entry = tk.Entry(self.preparation_frame, width=50)  # Make it accessible in other methods
        self.participant_entry.pack(pady=5)

        # Label and input for date
        date_label = tk.Label(self.preparation_frame, text="Date:")
        date_label.pack(pady=(10, 5))
        self.date_entry = tk.Entry(self.preparation_frame, width=50)  # Make it accessible in other methods
        self.date_entry.pack(pady=5)

        continue_button = tk.Button(self.preparation_frame, text="Save & Continue", command=self.show_monitoring_page)
        continue_button.pack(pady=20)

    def setup_monitoring_page(self):
        # Layout frame for buttons
        button_frame = tk.Frame(self.monitoring_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        
        start_button = tk.Button(button_frame, text="Start Recording")
        start_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        stop_button = tk.Button(button_frame, text="Stop Recording", command=self.show_statistics_page)
        stop_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Layout frame for visualization and camera feed
        content_frame = tk.Frame(self.monitoring_frame)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Matplotlib figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        self.scat_left, = ax1.plot([], [], 'o', label='Left Pupil Diameter')
        self.scat_right, = ax1.plot([], [], 'o', label='Right Pupil Diameter')
        self.line_left, = ax2.plot([], [], '-', label='Left Eyelid Opening')
        self.line_right, = ax2.plot([], '-', label='Right Eyelid Opening')

        ax1.legend()
        ax2.legend()
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Pupil Diameter')
        ax2.set_ylabel('Eyelid Opening')

        plot_frame = tk.Frame(content_frame)
        plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ani = FuncAnimation(fig, self.update_plot, interval=100)

        # Camera feed
        camera_frame = tk.Frame(content_frame)
        camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.camera_label = Label(camera_frame)
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        self.cap = cv2.VideoCapture(0)  # Start video capture on default camera
        self.update_camera()

    def update_camera(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()
        if ret:
            # Convert image to RGB (OpenCV uses BGR by default)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.camera_label.after(10, self.update_camera)  # Refresh camera frame every 10ms

    def setup_statistics_page(self):
        return_button = tk.Button(self.statistics_frame, text="Return to Monitoring", command=self.return_to_monitoring)
        return_button.pack(pady=20, padx=20)

    def show_monitoring_page(self):
        participant_info = self.participant_entry.get()
        date_info = self.date_entry.get()
        self.date=date_info
        self.subject = participant_info
        data_to_send = json.dumps({"participant": participant_info, "date": date_info})
        print(data_to_send)
        self.send_data(data_to_send)
        # Switch to monitoring page
        self.preparation_frame.pack_forget()
        self.monitoring_frame.pack(fill='both', expand=True)

    def show_statistics_page(self):
        self.monitoring_frame.pack_forget()
        self.statistics_frame.pack(fill='both', expand=True)

    def return_to_monitoring(self):
        self.statistics_frame.pack_forget()
        self.monitoring_frame.pack(fill='both', expand=True)
        
    def send_data(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data.encode(), ('127.0.0.1', 2005))
            
    def update_plot(self, frame):
        data, addr = self.sock.recvfrom(8192) 
        json_data = json.loads(data.decode())

        self.times.append(len(self.times) + 1)
        self.left_pupil_diameters.append(json_data['LeftPupilDiameter'])
        self.right_pupil_diameters.append(json_data['RightPupilDiameter'])
        self.left_eyelid_openings.append(json_data['LeftEyelidOpening'])
        self.right_eyelid_openings.append(json_data['RightEyelidOpening'])

        self.scat_left.set_data(range(len(self.times)), self.left_pupil_diameters)
        self.scat_right.set_data(range(len(self.times)), self.right_pupil_diameters)
        self.line_left.set_data(range(len(self.times)), self.left_eyelid_openings)
        self.line_right.set_data(range(len(self.times)), self.right_eyelid_openings)

        self.canvas.figure.axes[0].relim()
        self.canvas.figure.axes[0].autoscale_view()
        self.canvas.figure.axes[1].relim()
        self.canvas.figure.axes[1].autoscale_view()
        self.canvas.draw()

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
