import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.dates import DateFormatter

def load_and_clean_data(data_path, skip_rows=10):
    data = pd.read_csv(data_path).iloc[skip_rows:]
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
    return data

def plot_arousal_and_brainwaves(ax, data, takeover_times, collision_times):
    ax.plot(data['timestamp'], data['arousal'], 'cornflowerblue', label='arousal', linewidth=0.5)
    ax.set_ylabel('Arousal')
    ax.set_xlabel('Timestamp')
    ax.set_title('Brain EEG Averages with Arousal Highlighted')
    ax.grid(True)

    ax2 = ax.twinx()
    colors = ['blue', 'green', 'purple', 'orange']
    for idx, column in enumerate(['alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg']):
        ax2.plot(data['timestamp'], data[column], label=column, alpha=0.2, color=colors[idx])
    ax2.set_ylabel('Brain Wave Averages')

    # Marking Takeovers
    for time in takeover_times:
        ax.axvline(x=time, color='lightcoral', linestyle='--', label='Take over')

    # Marking Collisions
    for time in collision_times:
        ax.axvline(x=time, color='black', linestyle='-.',linewidth=0.5)

    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

def plot_speed_with_mode_switch(ax, data):
    data.set_index('Time', inplace=True)
    
    ax.plot(data.index, data['Speed'], label='Speed', color='mediumseagreen', linestyle='-')
    mode_switch_times = data[data['Mode_Switched'] == 'Yes'].index

    # Marking Takeovers and Collisions
    for time in mode_switch_times:
        ax.axvline(x=time, color='lightcoral', linestyle='--', label='Take over')
    
    collision_times = data[data['Collision'] == 'Yes'].index
    for time in collision_times:
        ax.axvline(x=time, color='black', linestyle='-.',linewidth=0.5)

    ax.set_title('Speed Over Time with Mode Switch Indicators')
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed')
    ax.legend()
    ax.grid(True)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

def main():
    script_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    eeg_data_path = os.path.join(script_path, 'data', 'data_psd_0425_02.csv')
    eeg_data = load_and_clean_data(eeg_data_path)

    vehicle_data_path = os.path.join(script_path, 'data', 'mainvehicle_20240425170754_1.csv')
    vehicle_data = pd.read_csv(vehicle_data_path)
    vehicle_data['Time'] = pd.to_datetime(vehicle_data['Time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)

    takeover_times = vehicle_data[vehicle_data['Mode_Switched'] == 'Yes']['Time'].tolist()
    collision_times = vehicle_data[vehicle_data['Collision'] == 'Yes']['Time'].tolist()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    plot_arousal_and_brainwaves(ax1, eeg_data, takeover_times, collision_times)
    plot_speed_with_mode_switch(ax2, vehicle_data)
    plt.subplots_adjust(hspace=0.5)
    plt.show()

if __name__ == '__main__':
    main()
