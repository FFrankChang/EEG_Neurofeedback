import tkinter as tk
import socket
import random

# Variable to store the last clicked condition
current_condition = "silence"

# Generate random conditions as previously defined
def generate_conditions():
    middle_conditions = ['silence'] * 5 + ['feedback'] * 5
    random.shuffle(middle_conditions)
    conditions = ['silence'] + middle_conditions + ['silence']
    return conditions

# Function to send UDP message, specifying port
def send_udp_message(message, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_host = "192.168.3.24"  # Host IP
    sock.sendto(message.encode(), (udp_host, port))
    print(f"'{message}' sent to port {port} {udp_host}")
    sock.close()

# Create the main window
root = tk.Tk()
root.title("Experiment Controller")

# Entry fields for subject and dd
subject_entry = tk.Entry(root, width=50)
subject_entry.pack(pady=5)
subject_entry.insert(0, "S01")

dd_entry = tk.Entry(root, width=50)
dd_entry.pack(pady=5)
dd_entry.insert(0, "D01")

# Create text widget for displaying conditions
text = tk.Text(root, height=12, width=50)
text.pack()

# Function to update current condition and send UDP message for conditions
def update_condition_and_send(condition):
    global current_condition
    current_condition = condition
    send_udp_message(condition, 12348)

# Condition buttons
silence_button = tk.Button(root, text="Silence", height=2, width=20,bg='grey',
                           command=lambda: update_condition_and_send("silence"))
silence_button.pack(pady=5)

feedback_button = tk.Button(root, text="Feedback", height=2, width=20,bg='light blue',
                            command=lambda: update_condition_and_send("feedback"))
feedback_button.pack(pady=5)

# Function to create buttons and send messages with subject, dd, and condition
def create_send_button(number, text):
    return tk.Button(root, text=text, height=2, width=20,
                     command=lambda: send_numeric_command(number))

def send_numeric_command(number):
    subject = subject_entry.get()
    dd = dd_entry.get()
    message = f"{number} | Condition: {current_condition} | Subject: {subject} | Day: {dd}"
    send_udp_message(message, 5005)
    if number == "0":
        send_udp_message("stop", 12348)
# Buttons for sending numeric commands with custom labels
button_labels = {
    "0": "Stop",
    "1": "Scenario Default",
    "2": "Scenario 01",
    "3": "Scenario 02"
}
for number, label in button_labels.items():
    btn = create_send_button(number, label)
    btn.pack(pady=2)

# Function to display conditions
def display_conditions():
    conditions = generate_conditions()
    text.delete('1.0', tk.END)  # Clear the text widget before displaying new conditions
    for i, condition in enumerate(conditions):
        text.insert(tk.END, f"Experiment {i+1}: {condition}\n")

# Display conditions on start
display_conditions()

# Button to refresh and redisplay conditions
refresh_button = tk.Button(root, text="Refresh Conditions", height=2, width=20,
                           command=display_conditions)
refresh_button.pack(pady=5)

# Start the GUI loop
root.mainloop()
