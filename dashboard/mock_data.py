from flask import Flask
from flask_socketio import SocketIO, emit
import random
import time
from threading import Thread, Event

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def generate_data(event_name):
    # This function generates random data and sends it to all connected clients
    while True:
        time.sleep(1)  # Simulate data generation interval
        data = {
            'time': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime()),  # ISO 8601 format
            'value': random.random() * 100  # Random value between 0 and 100
        }
        socketio.emit(event_name, data)  # Emit data to all clients subscribed to this event

@app.route('/')
def index():
    return "Real-time data visualization"

@socketio.on('connect')
def handle_connect():
    # Start a thread for each type of data when a client connects
    arousal_thread = Thread(target=generate_data, args=('arousal_data',))
    steering_thread = Thread(target=generate_data, args=('steering_data',))
    pupil_size_thread = Thread(target=generate_data, args=('pupilsize_data',))
    arousal_thread.start()
    steering_thread.start()
    pupil_size_thread.start()
    emit('my response', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
