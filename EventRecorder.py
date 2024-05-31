import tkinter as tk
import pandas as pd
from datetime import datetime

class EventRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Event Recorder")
        
        self.data = pd.DataFrame(columns=["Timestamp", "Type"])
        
        # 设置界面
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20)

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.listbox = tk.Listbox(self.frame, width=50, height=20, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 捕捉键盘事件
        self.master.bind('<space>', self.record_high)
        self.master.bind('l', self.record_low)
        self.master.bind('<Delete>', self.delete_last)

    def record_high(self, event):
        now = datetime.now()
        self.data.loc[len(self.data)] = [now, "High"]
        self.listbox.insert(tk.END, f"{now} - High")
        self.listbox.see(tk.END)  # 滚动到最新的条目

    def record_low(self, event):
        now = datetime.now()
        self.data.loc[len(self.data)] = [now, "Low"]
        self.listbox.insert(tk.END, f"{now} - Low")
        self.listbox.see(tk.END)  # 滚动到最新的条目

    def delete_last(self, event):
        if not self.data.empty:
            self.data.drop(self.data.index[-1], inplace=True)
            self.listbox.delete(tk.END)

    def save_data(self):
        filename = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

def on_closing():
    app.save_data()
    root.destroy()

root = tk.Tk()
app = EventRecorder(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
