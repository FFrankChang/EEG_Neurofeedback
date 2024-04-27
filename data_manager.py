import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

class DataVisualizer:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def plot_arousal_and_brainwaves(self, ax):
        """Plot arousal and brainwaves on given axes."""
        data = self.data_manager.sync_data()  # Assuming this method exists and syncs the relevant EEG data
        ax.plot(data['timestamp'], data['arousal'], 'cornflowerblue', label='arousal', linewidth=0.5)
        ax.set_ylabel('Arousal')
        ax.set_xlabel('Timestamp')
        ax.set_title('Brain EEG Averages with Arousal Highlighted')
        ax.grid(True)

        ax2 = ax.twinx()
        colors = ['blue', 'green', 'purple', 'orange']
        brainwave_columns = ['alpha_avg', 'beta_avg', 'theta_avg', 'delta_avg']  # Ensure these columns exist in your data
        for idx, column in enumerate(brainwave_columns):
            ax2.plot(data['timestamp'], data[column], label=column, alpha=0.2, color=colors[idx], linewidth=0.5)
        ax2.set_ylabel('Brain Wave Averages')

        for time in self.data_manager.mode_times:
            ax.axvline(x=time, color='lightcoral', linestyle='--', label='Take over')
        for time in self.data_manager.collision_times:
            ax.axvline(x=time, color='black', linestyle='-.')

        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    def plot_speed_with_mode_switch(self, ax):
        """Plot vehicle speeds and mode switches on given axes."""
        data = self.data_manager.sync_data()  # Assuming sync_data appropriately combines vehicle data
        ax.plot(data['timestamp'], data['Speed'], label='Main Vehicle Speed', color='mediumseagreen', linestyle=':', alpha=0.5)
        ax.plot(data['timestamp'], data['Lead_Vehicle_Speed'], label='Lead Vehicle Speed', color='royalblue', linestyle=':', alpha=0.5)

        for time in self.data_manager.mode_times:
            ax.axvline(x=time, color='lightcoral', linestyle='--', label='Take over')
        for time in self.data_manager.collision_times:
            ax.axvline(x=time, color='black', linestyle='-.')

        ax.set_title('Speed Over Time with TTC')
        ax.set_xlabel('Time')
        ax.set_ylabel('Speed')
        ax.legend(loc='upper left')
        ax.grid(True)
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

        ax2 = ax.twinx()
        ax2.plot(data['timestamp'], data['TTC'], label='TTC', color='purple', linestyle='-')
        ax2.set_ylabel('TTC (s)')
        ax2.set_yscale('log')
        ax2.legend(loc='upper right')

    def plot_pupil_diameters(self, ax):
        """Plot smoothed pupil diameters with event markers."""
        df = self.data_manager.eye_data
        df['smoothed_left'] = df['smarteye|LeftPupilDiameter'].rolling(window=10, center=True).mean()
        df['smoothed_right'] = df['smarteye|RightPupilDiameter'].rolling(window=10, center=True).mean()

        ax.plot(df['timestamp'], df['smoothed_left'], label='Smoothed Left Pupil Diameter', linewidth=0.5)
        ax.plot(df['timestamp'], df['smoothed_right'], label='Smoothed Right Pupil Diameter', linewidth=0.5)
        
        # Add event markers
        for time in self.data_manager.mode_times:
            ax.axvline(x=time, color='lightcoral', linestyle='--', label='Mode Switched')
        for time in self.data_manager.collision_times:
            ax.axvline(x=time, color='black', linestyle='-.', label='Collision')

        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Pupil Diameter')
        ax.set_title('Smoothed Pupil Diameter Over Time')
        ax.legend()

    def plot_heart_rate(self, ax):
        """Plot heart rate over time with event markers."""
        ecg_values = self.data_manager.ecg_data['BIP 01'].values
        peaks, _ = find_peaks(ecg_values, distance=1000 / 2)  # Assuming a sampling rate
        heart_rate_times = self.data_manager.ecg_data['timestamp'].iloc[peaks]
        rr_intervals = np.diff(peaks) / 1000 * 1000
        heart_rate = 60 / (rr_intervals / 1000)

        ax.plot(heart_rate_times, heart_rate, label='Heart Rate', color='red')
        
        # Add event markers
        for time in self.data_manager.mode_times:
            ax.axvline(x=time, color='lightcoral', linestyle='--', label='Mode Switched')
        for time in self.data_manager.collision_times:
            ax.axvline(x=time, color='black', linestyle='-.', label='Collision')

        ax.set_xlabel('Time')
        ax.set_ylabel('Heart Rate (beats per minute)')
        ax.set_title('Heart Rate Over Time')
        ax.legend()


    def visualize(self, plots=['brainwaves', 'speed', 'pupil', 'heart']):
        """Visualize selected plots."""
        fig, axs = plt.subplots(len(plots), 1, figsize=(10, 5 * len(plots)))
        if len(plots) == 1:
            axs = [axs]  # Make sure axs is always a list

        for i, plot in enumerate(plots):
            if plot == 'brainwaves':
                self.plot_brainwaves(axs[i])
            elif plot == 'speed':
                self.plot_vehicle_speed(axs[i])
            elif plot == 'pupil':
                self.plot_pupil_diameters(axs[i])
            elif plot == 'heart':
                self.plot_heart_rate(axs[i])

        fig.tight_layout()
        plt.show()

# Example usage
# dm = DataManager('path_to_eye.csv', 'path_to_carla.csv', 'path_to_eeg.csv')
# dv = DataVisualizer(dm)
# dv.visualize()
