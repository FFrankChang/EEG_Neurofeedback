import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import os
class DataVisualizer:
    def __init__(self, data_manager):
        self.data_manager = data_manager


    def plot_arousal(self, ax):
        if self.data_manager.eeg_data is None:
            raise ValueError("EEG data has not been loaded.")
        data = self.data_manager.eeg_data
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)


        ax.plot(data['timestamp'], data['arousal'], 'red', label='Arousal', linewidth=1, alpha=0.2)

        smoothed_arousal = data['arousal'].rolling(window=20, center=True).mean()
        ax.plot(data['timestamp'], smoothed_arousal, 'lightcoral', label='Smoothed Arousal', linewidth=1)

        ax.set_ylabel('Arousal')
        ax.set_title('Brain EEG Averages with Arousal Highlighted')
        ax.grid(True)

        # ax2 = ax.twinx()
        # colors = ['blue', 'green', 'purple', 'gold']
        # brainwave_columns = ['F7_arousal','F8_arousal','P7_arousal','P8_arousal'] 
        # for idx, column in enumerate(brainwave_columns):
        #     ax2.plot(data['timestamp'], data[column], label=column, alpha=0.1, color=colors[idx], linewidth=0.5)
        # ax2.set_ylabel('Single channel')

        self.plot_event_markers(ax)

        ax.legend(loc='upper left')
        # ax2.legend(loc='upper right')
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    def plot_carla(self, ax):
        if self.data_manager.carla_data is None:
            raise ValueError("Carla data has not been loaded.")
        data = self.data_manager.carla_data
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
        ax.plot(data['timestamp'], data['Speed'], label='Main Vehicle Speed', color='mediumseagreen', linestyle=':', alpha=0.5)
        ax.plot(data['timestamp'], data['Lead_Vehicle_Speed'], label='Lead Vehicle Speed', color='royalblue', linestyle=':', alpha=0.5)
        self.plot_deceleration_periods(ax)
        self.plot_event_markers(ax)

        ax.set_title('Speed Over Time with TTC')
        ax.set_ylabel('Speed')
        ax.legend(loc='upper left')
        ax.grid(True)
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

        ax2 = ax.twinx()
        ax2.plot(data['timestamp'], data['TTC'], label='TTC', color='purple', linestyle='-',linewidth=0.5)
        ax2.set_ylabel('TTC (s)')
        ax2.set_yscale('log')
        ax2.legend(loc='upper right')

    def plot_eye(self, ax):
        if self.data_manager.eye_data is None:
            raise ValueError("Eye data has not been loaded.")
        df = self.data_manager.eye_data
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)
        df['smoothed_left'] = df['smarteye|LeftPupilDiameter'].rolling(window=10, center=True).mean()
        df['smoothed_right'] = df['smarteye|RightPupilDiameter'].rolling(window=10, center=True).mean()

        ax.plot(df['timestamp'], df['smoothed_left'], label='Smoothed Left Pupil Diameter', linewidth=0.5)
        ax.plot(df['timestamp'], df['smoothed_right'], label='Smoothed Right Pupil Diameter', linewidth=0.5)
        
        self.plot_event_markers(ax)

        ax.set_ylabel('Pupil Diameter')
        ax.set_title('Smoothed Pupil Diameter Over Time')
        ax.legend(loc='upper left')
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    def plot_heart(self, ax):
        if self.data_manager.heart_rate_data is None:
            raise ValueError("Heart rate data has not been loaded.")
        heart_rate_data = self.data_manager.heart_rate_data
        heart_rate_data['time'] = pd.to_datetime(heart_rate_data['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai').dt.tz_localize(None)

        ax.plot(heart_rate_data['time'], heart_rate_data['heart_rate'], label='Heart Rate', color='cornflowerblue', linewidth=0.5)

        # Compute and draw horizontal lines for average heart rate for each segment
        for start, end in zip([heart_rate_data['time'].iloc[0]] + self.data_manager.mode_times, self.data_manager.mode_times + [heart_rate_data['time'].iloc[-1]]):
            mask = (heart_rate_data['time'] >= start) & (heart_rate_data['time'] < end)
            segment_hr = heart_rate_data['heart_rate'][mask]
            if not segment_hr.empty:
                avg_hr = segment_hr.mean()
                ax.hlines(avg_hr, start, end, colors='blue', linewidth=1, linestyles='--', alpha=0.5, label='Average HR' if 'Average HR' not in ax.get_legend_handles_labels()[1] else '')

        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        self.plot_event_markers(ax)

        ax.set_ylabel('Heart Rate (beats per minute)')
        ax.set_title('Heart Rate Over Time')
        ax.legend()

    def plot_event_markers(self, ax):
        """Plot event markers for mode switched and collisions."""
        if self.data_manager.mode_times:
            for time in self.data_manager.mode_times:
                ax.axvline(x=time, color='red', linestyle='--', label='Mode Switched' if 'Mode Switched' not in ax.get_legend_handles_labels()[1] else '')
        if self.data_manager.collision_times:
            for time in self.data_manager.collision_times:
                ax.axvline(x=time, color='black', linestyle='-.', label='Collision' if 'Collision' not in ax.get_legend_handles_labels()[1] else '')
    
    def plot_deceleration_periods(self, ax):
        """Highlights deceleration periods on the plot."""
        for start, end in self.data_manager.deceleration_periods:
            start = pd.to_datetime(start, unit='s').tz_localize('UTC').tz_convert('Asia/Shanghai').tz_localize(None)
            end = pd.to_datetime(end, unit='s').tz_localize('UTC').tz_convert('Asia/Shanghai').tz_localize(None)
            ax.axvspan(start, end, color='grey',alpha = 0.3)

    def visualize(self, plots=['arousal', 'carla', 'eye', 'heart'],display= True):
        """Visualize selected plots only if data is loaded."""
        fig, axs = plt.subplots(len(plots), 1, figsize=(18, 3 * len(plots)))
        
        if len(plots) == 1:
            axs = [axs]
        for i, plot in enumerate(plots):
            plot_func = getattr(self, f'plot_{plot}', None)
            if plot_func :
                plot_func(axs[i])
            else:
                raise ValueError(f"{plot.capitalize()} data has not been loaded, cannot visualize.")
        axs[-1].set_xlabel('Time') 
        fig.tight_layout()
        plt.subplots_adjust(hspace=0.3, top=0.92)
        fig.suptitle(self.data_manager.folder_name,fontweight='bold')
        plt.get_current_fig_manager().window.state('zoomed')
        if display:
            plt.show()
        return fig
    
    def save_figure(self, fig, path=None):
        """Save the figure to the default directory or an additional path if provided."""
        default_filename = os.path.join(self.data_manager.data_dir, self.data_manager.folder_name + '_overall.png')
        # fig.savefig(default_filename)
        # print(f"Figure saved to {default_filename}")
        if path:
            additional_filename = os.path.join(path, self.data_manager.folder_name + '_overall.png')
            fig.savefig(additional_filename)
            print(f"Figure also saved to {additional_filename}")