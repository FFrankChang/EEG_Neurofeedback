import socket
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Setting up the UDP server
UDP_IP = "127.0.0.1"
UDP_PORT = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Prepare the plot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
scat_left, = ax1.plot([], [], 'o', label='Left Pupil Diameter')
scat_right, = ax1.plot([], [], 'o', label='Right Pupil Diameter')
line_left, = ax2.plot([], [], '-', label='Left Eyelid Opening')
line_right, = ax2.plot([], [], '-', label='Right Eyelid Opening')

ax1.legend()
ax2.legend()
ax1.set_xlabel('Time')
ax1.set_ylabel('Pupil Diameter')
ax2.set_ylabel('Eyelid Opening')

# Initialize deques to store data with a maximum length of 180
max_points = 120
times = deque(maxlen=max_points)
left_pupil_diameters = deque(maxlen=max_points)
right_pupil_diameters = deque(maxlen=max_points)
left_eyelid_openings = deque(maxlen=max_points)
right_eyelid_openings = deque(maxlen=max_points)

# Animation update function
def update(frame):
    data, addr = sock.recvfrom(8192) 
    json_data = json.loads(data.decode())
    
    # Update deques with new data
    times.append(len(times) + 1)  # This increments time points linearly, adjust as necessary
    left_pupil_diameters.append(json_data['LeftPupilDiameter'])
    right_pupil_diameters.append(json_data['RightPupilDiameter'])
    left_eyelid_openings.append(json_data['LeftEyelidOpening'])
    right_eyelid_openings.append(json_data['RightEyelidOpening'])
    
    # Update plot data
    scat_left.set_data(range(len(times)), left_pupil_diameters)
    scat_right.set_data(range(len(times)), right_pupil_diameters)
    line_left.set_data(range(len(times)), left_eyelid_openings)
    line_right.set_data(range(len(times)), right_eyelid_openings)
    
    # Rescale the plot
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    return scat_left, scat_right, line_left, line_right

# Run the animation
ani = FuncAnimation(fig, update, interval=100)  # Update interval in milliseconds
plt.show()
