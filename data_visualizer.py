import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from scipy.signal import find_peaks
import pandas as pd
import numpy as np

class DataVisualizer:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def plot_arousal_and_brainwaves(self, ax):
        """Plot arousal and brainwaves on given axes."""
        data = self.data_manager.eeg_data
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
        ax.plot(data['timestamp'], data['arousal'], 'lightcoral', label='arousal', linewidth=1)
        ax.set_ylabel('Arousal')
        ax.set_xlabel('Time')
        ax.set_title('Brain EEG Averages with Arousal Highlighted')
        ax.grid(True)

        ax2 = ax.twinx()
        colors = ['blue', 'green', 'purple', 'gold']
        brainwave_columns = ['alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg']  # Ensure these columns exist in your data
        for idx, column in enumerate(brainwave_columns):
            ax2.plot(data['timestamp'], data[column], label=column, alpha=0.2, color=colors[idx], linewidth=0.5)
        ax2.set_ylabel('Brain Wave Averages')

        self.plot_event_markers(ax)

        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    def plot_speed_with_mode_switch(self, ax):
        """Plot vehicle speeds and mode switches on given axes."""
        data = self.data_manager.carla_data
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
        ax.plot(data['timestamp'], data['Speed'], label='Main Vehicle Speed', color='mediumseagreen', linestyle=':', alpha=0.5)
        ax.plot(data['timestamp'], data['Lead_Vehicle_Speed'], label='Lead Vehicle Speed', color='royalblue', linestyle=':', alpha=0.5)

        self.plot_event_markers(ax)

        ax.set_title('Speed Over Time with TTC')
        ax.set_xlabel('Time')
        ax.set_ylabel('Speed')
        ax.legend(loc='upper left')
        ax.grid(True)
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

        ax2 = ax.twinx()
        ax2.plot(data['timestamp'], data['TTC'], label='TTC', color='purple', linestyle='-',linewidth=0.5)
        ax2.set_ylabel('TTC (s)')
        ax2.set_yscale('log')
        ax2.legend(loc='upper right')

    def plot_pupil_diameters(self, ax):
        """Plot smoothed pupil diameters with event markers."""
        df = self.data_manager.eye_data
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)

        df['smoothed_left'] = df['smarteye|LeftPupilDiameter'].rolling(window=10, center=True).mean()
        df['smoothed_right'] = df['smarteye|RightPupilDiameter'].rolling(window=10, center=True).mean()

        ax.plot(df['timestamp'], df['smoothed_left'], label='Smoothed Left Pupil Diameter', linewidth=0.5)
        ax.plot(df['timestamp'], df['smoothed_right'], label='Smoothed Right Pupil Diameter', linewidth=0.5)
        
        self.plot_event_markers(ax)

        ax.set_xlabel('Time')
        ax.set_ylabel('Pupil Diameter')
        ax.set_title('Smoothed Pupil Diameter Over Time')
        ax.legend(loc='upper left')
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))


    def plot_heart_rate(self, ax):
        """Plot heart rate over time with event markers and average heart rate between mode switches displayed as horizontal lines."""
        ecg_values = self.data_manager.ecg_data['BIP 01'].values
        peaks, _ = find_peaks(ecg_values, distance=1000 / 2)
        self.data_manager.ecg_data['time'] = pd.to_datetime(self.data_manager.ecg_data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)

        heart_rate_times = self.data_manager.ecg_data['time'].iloc[peaks]  # Use full range of peaks
        rr_intervals = np.diff(peaks) / 1000
        heart_rate = 60 / rr_intervals
        heart_rate_times = heart_rate_times[1:]  # Adjust time points to match heart rate data size right before plotting

        ax.plot(heart_rate_times, heart_rate, label='Heart Rate', color='cornflowerblue', linewidth=0.5)

        mode_times = self.data_manager.mode_times
        if len(mode_times) > 0:
            all_times = [heart_rate_times.iloc[0]] + mode_times + [heart_rate_times.iloc[-1]]
        else:
            all_times = [heart_rate_times.iloc[0], heart_rate_times.iloc[-1]]

        # Compute and draw horizontal lines for average heart rate for each segment
        for start, end in zip(all_times[:-1], all_times[1:]):
            mask = (heart_rate_times >= start) & (heart_rate_times < end)
            segment_hr = heart_rate[mask]
            if len(segment_hr) > 0:
                avg_hr = np.mean(segment_hr)
                ax.hlines(avg_hr, start, end, colors='blue', linewidth=1, linestyles='--',alpha=0.5, label='Average HR' if 'Average HR' not in ax.get_legend_handles_labels()[1] else '')
        
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        self.plot_event_markers(ax)

        ax.set_xlabel('Time')
        ax.set_ylabel('Heart Rate (beats per minute)')
        ax.set_title('Heart Rate Over Time')
        ax.legend()

    def plot_event_markers(self,ax):
        """Plot event markers for mode switched and collisions."""
        for time in self.data_manager.mode_times:
            ax.axvline(x=time, color='red', linestyle='--', label='Mode Switched' if 'Mode Switched' not in ax.get_legend_handles_labels()[1] else '')
        for time in self.data_manager.collision_times:
            ax.axvline(x=time, color='black', linestyle='-.', label='Collision' if 'Collision' not in ax.get_legend_handles_labels()[1] else '')

    def visualize(self, plots=['brainwaves', 'speed', 'pupil', 'heart']):
        """Visualize selected plots."""
        fig, axs = plt.subplots(len(plots), 1, sharex=True,figsize=(10, 5 * len(plots)))
        if len(plots) == 1:
            axs = [axs]  # Make sure axs is always a list

        for i, plot in enumerate(plots):
            if plot == 'brainwaves':
                self.plot_arousal_and_brainwaves(axs[i])
            elif plot == 'speed':
                self.plot_speed_with_mode_switch(axs[i])
            elif plot == 'pupil':
                self.plot_pupil_diameters(axs[i])
            elif plot == 'heart':
                self.plot_heart_rate(axs[i])

        fig.tight_layout()
        plt.subplots_adjust(hspace=0.3)
        plt.get_current_fig_manager().window.state('zoomed')
        plt.show()
