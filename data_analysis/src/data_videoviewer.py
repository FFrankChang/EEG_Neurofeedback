import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
from matplotlib.lines import Line2D

from data_manager import DataManager
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
    def __init__(self, video_path, data_manager, start_time, visualizations):
        super().__init__()
        self.title("Video and Data Viewer")
        self.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        self.data_manager = data_manager
        self.visualizer = DataVisualizer(data_manager)  
        self.visualizations = visualizations
        
        self.cap = cv2.VideoCapture(video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.current_frame = 0  
        self.create_widgets()
        self.update_video(self.current_frame)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", lambda event: self.on_close())
        self.bind("<Right>", self.next_frame)
        self.bind("<Left>", self.previous_frame)

    def create_widgets(self):
        self.video_label = tk.Label(self)
        self.video_label.grid(row=0, column=0, sticky='ewns')

        self.slider = ttk.Scale(self, from_=0, to=self.total_frames - 1, orient='horizontal', command=self.slider_moved)
        self.slider.grid(row=1, column=0, sticky='ew')

        self.timestamp_label = tk.Label(self, text="")
        self.timestamp_label.grid(row=2, column=0, sticky='ew')

        self.fig, self.axs = plt.subplots(len(self.visualizations), 1, figsize=(10, 5 * len(self.visualizations)), sharex=True)
        if len(self.visualizations) == 1:
            self.axs = [self.axs]  # Ensure axs is always a list
        for i, plot in enumerate(self.visualizations):
            getattr(self.visualizer, f'plot_{plot}')(self.axs[i])
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=3, sticky='ewns')

        self.lines = [ax.axvline(self.start_time, color='lime') for ax in self.axs]

    def slider_moved(self, value):
        self.update_video(int(float(value)))
        
    def next_frame(self, event):
        """移动到下一帧"""
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
            self.update_video(self.current_frame)
            self.slider.set(self.current_frame)

    def previous_frame(self, event):
        """移动到上一帧"""
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update_video(self.current_frame)
            self.slider.set(self.current_frame)

    def update_video(self, frame):
        """更新视频帧并调整尺寸以适应界面"""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, image = self.cap.read()
        if ret:
            image = resize_frame(image)  # 确保已经定义了resize_frame函数
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            time_offset = frame / self.fps
            current_frame_time = self.start_time + datetime.timedelta(seconds=time_offset)
            self.timestamp_label.config(text=current_frame_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

            for line in self.lines:
                line.set_xdata([current_frame_time, current_frame_time])
            self.fig.canvas.draw_idle()

    def on_close(self):
        """关闭视频捕捉和窗口"""
        self.cap.release()
        self.destroy()
        self.quit()

    def on_escape(self):
        self.on_close()