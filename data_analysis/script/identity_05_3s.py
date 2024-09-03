import pandas as pd
import matplotlib.pyplot as plt

class VehicleDataProcessor:
    def __init__(self, file_path):
        self.carla_data = pd.read_csv(file_path)
        self.deceleration_periods = []

    def fill_missing_values(self):
        """Fill missing values in the 'Mode_Switched' column."""
        self.carla_data['Mode_Switched'] = self.carla_data['Mode_Switched'].fillna("No")

    def detect_deceleration_periods(self):
        """Detects continuous deceleration periods based on speed thresholds."""
        self.fill_missing_values()
        switch_indices = self.carla_data.index[self.carla_data['Mode_Switched'].eq("Yes")]
        temp_periods = []
        for index in switch_indices:
            subset = self.carla_data.loc[index:].reset_index(drop=True)
            speed_less_than_75 = subset['Lead_Vehicle_Speed'] < 75
            in_deceleration = False
            start_time = None
            
            for i, (time, speed, is_below_threshold) in enumerate(zip(subset['timestamp'], subset['Lead_Vehicle_Speed'], speed_less_than_75)):
                if is_below_threshold and not in_deceleration:
                    in_deceleration = True
                    start_time = time
                elif not is_below_threshold and in_deceleration:
                    in_deceleration = False
                    if start_time:
                        end_time = subset['timestamp'][i-1] + 1  
                        temp_periods.append((start_time, end_time))
            
            if in_deceleration and start_time:
                end_time = subset['timestamp'].iloc[-1] + 1
                temp_periods.append((start_time, end_time))

        if temp_periods:
            merged_periods = [temp_periods[0]]
            for start, end in temp_periods[1:]:
                last_end = merged_periods[-1][1]
                if start - last_end <= 0.5:
                    merged_periods[-1] = (merged_periods[-1][0], end)
                else:
                    merged_periods.append((start, end))

            self.deceleration_periods = merged_periods

    def plot_trajectory(self):
        """Plot the vehicle trajectory and deceleration periods."""
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.plot(self.carla_data['Location_x'], self.carla_data['Location_y'], label='Trajectory', color='lightblue', linestyle='--')

        for start_time, end_time in self.deceleration_periods:
            start_index_list = self.carla_data[self.carla_data['timestamp'] == start_time].index.tolist()
            end_index_list = self.carla_data[self.carla_data['timestamp'] == end_time].index.tolist()

            # 如果找不到确切的结束时间，取最接近的小于该时间的最后一个索引
            if not end_index_list:
                end_index_list = [self.carla_data[self.carla_data['timestamp'] < end_time].index[-1]]

            if start_index_list and end_index_list:  # 确保开始和结束时间都有效
                start_index = start_index_list[0]
                end_index = end_index_list[0]
                ax.plot(self.carla_data['Location_x'][start_index:end_index], self.carla_data['Location_y'][start_index:end_index], label='Deceleration', color='steelblue', linewidth=2)
            
        for line in [2992.5, 2996.25, 3000, 3003.75, 3007.5, 3011.25]:
            ax.axhline(y=line, color='grey', linestyle='-', linewidth=0.5)
        ax.set_xlim(5500, 3000)
        ax.set_ylim(2970, 3030)
        ax.set(xlabel='Location X', ylabel='Location Y')
        ax.set_title('Selected Event')
        plt.show()

# Load and process data
file_path = r"E:\NFB_data_backup\data_20240606\test\20240531_lxk_05_easy_silence\carla_merged.csv"
processor = VehicleDataProcessor(file_path)
processor.detect_deceleration_periods()
processor.plot_trajectory()
