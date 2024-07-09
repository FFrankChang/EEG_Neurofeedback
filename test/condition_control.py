import tkinter as tk
import socket
import random

# Generate random conditions as previously defined
def generate_conditions():
    middle_conditions = ['silence'] * 5 + ['feedback'] * 5
    random.shuffle(middle_conditions)
    conditions = ['silence'] + middle_conditions + ['silence']
    return conditions

# Function to send UDP message
def send_udp_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_host = "localhost"  # Host IP
    udp_port = 12348         # Specified port to connect
    sock.sendto(message.encode(), (udp_host, udp_port))
    print(message+' sent')
    sock.close()

# Create the main window
root = tk.Tk()
root.title("Experiment Controller")

# Create text widget
text = tk.Text(root, height=12, width=50)
text.pack()

# Button to send "silence" message
silence_button = tk.Button(root, text="Silence", command=lambda: send_udp_message("silence"))
silence_button.pack(pady=5)

# Button to send "feedback" message
feedback_button = tk.Button(root, text="Feedback", command=lambda: send_udp_message("feedback"))
feedback_button.pack(pady=5)

# Function to display conditions
def display_conditions():
    conditions = generate_conditions()
    for i, condition in enumerate(conditions):
        text.insert(tk.END, f"Experiment {i+1}: {condition}\n")

# Display conditions on start
display_conditions()

# Start the GUI loop
root.mainloop()
