import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import pytesseract
import re
from data_visualizer import DataVisualizer

def resize_frame(image, max_length=640):
    height, width = image.shape[:2]
    if max(height, width) > max_length:
        scale = max_length / max(height, width)
        new_height = int(height * scale)
        new_width = int(width * scale)
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized
    return image

class VideoDataViewer(tk.Tk):
    def __init__(self, video_path, data_manager, visualizations, start_time=None):
        super().__init__()
        self.title("Video and Data Viewer")
        self.data_manager = data_manager
        self.visualizer = DataVisualizer(data_manager)
        self.visualizations = visualizations
        
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError("Error opening video file")
        
        if start_time is None:
            self.start_time = self.extract_start_time()
        else:
            if isinstance(start_time, str):
                self.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
            else:
                self.start_time = start_time

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.current_frame = 0 
        self.create_widgets()
        self.update_video(self.current_frame)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", lambda event: self.on_close())
        self.bind("<Right>", self.next_frame)
        self.bind("<Left>", self.previous_frame)

    def extract_start_time(self):
        ret, frame = self.cap.read()
        if ret:
            text = pytesseract.image_to_string(frame, config='--oem 3 --psm 6')
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            time_pattern = r'\d{2}:\d{2}:\d{2}:\d{3}'
            date_match = re.search(date_pattern, text)
            time_match = re.search(time_pattern, text)
            if date_match and time_match:
                formatted_time = time_match.group(0)[:-4] + '.' + time_match.group(0)[-3:]
                start_time_str = f"{date_match.group(0)} {formatted_time}"
                return datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")
            else:
                raise ValueError("Failed to extract date and time from video frame")
        else:
            raise ValueError("Failed to read the first frame")
        return None
    
    def create_widgets(self):
        self.video_label = tk.Label(self)
        self.video_label.grid(row=0, column=0, sticky='ewns')

        self.slider = ttk.Scale(self, from_=0, to=self.total_frames - 1, orient='horizontal', command=self.slider_moved)
        self.slider.grid(row=1, column=0, sticky='ew')

        self.timestamp_label = tk.Label(self, text="")
        self.timestamp_label.grid(row=2, column=0, sticky='ew')

        self.fig, self.axs = plt.subplots(len(self.visualizations), 1, figsize=(10, 5 * len(self.visualizations)), sharex=True)
        if len(self.visualizations) == 1:
            self.axs = [self.axs]
        for i, plot in enumerate(self.visualizations):
            getattr(self.visualizer, f'plot_{plot}')(self.axs[i])
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=3, sticky='ewns')

        self.lines = [ax.axvline(self.start_time, color='lime') for ax in self.axs]
        buffer_time = datetime.timedelta(seconds=1)
        data_start_time = self.data_manager.eeg_data['timestamp'].min() - buffer_time
        data_end_time = self.data_manager.eeg_data['timestamp'].max() + buffer_time
        for ax in self.axs:
            ax.set_xlim([data_start_time, data_end_time])

    def slider_moved(self, value):
        self.update_video(int(float(value)))
        self.current_frame = int(float(value))

    def next_frame(self, event):
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
            self.update_video(self.current_frame)
            self.slider.set(self.current_frame)

    def previous_frame(self, event):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update_video(self.current_frame)
            self.slider.set(self.current_frame)

    def update_video(self, frame):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, image = self.cap.read()
        if ret:
            image = resize_frame(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            time_offset = frame / self.fps
            current_frame_time = self.start_time + datetime.timedelta(seconds=time_offset)
            self.timestamp_label.config(text=current_frame_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
            min_time = self.data_manager.eeg_data['timestamp'].min()
            max_time = self.data_manager.eeg_data['timestamp'].max()

            if current_frame_time < min_time:
                line_time = min_time
            elif current_frame_time > max_time:
                line_time = max_time
            else:
                line_time = current_frame_time

            for line in self.lines:
                line.set_xdata([line_time, line_time])
            self.fig.canvas.draw_idle()

    def on_close(self):
        self.cap.release()
        self.destroy()
        self.quit()
