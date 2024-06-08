import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

for i in range(1,11):
    subject = 's' + str(i).zfill(2)

    file_path = rf'E:\EEG_Neurofeedback\data_analysis\results\20240606\+3sresults\{subject}_+3sresults.csv'  # Update this to your actual file path
    data = pd.read_csv(file_path)


    # 获取文件名作为图的标题
    file_name = os.path.basename(file_path).split('.')[0]  # 从路径中提取文件名，去掉后缀

    # 筛选出不同scenario的数据
    hard_data = data[data['condition'] == 'silence']
    easy_data = data[data['condition'] == 'feedback']

    # Adding a row index for plotting purposes
    hard_data['row_index'] = np.arange(len(hard_data))
    easy_data['row_index'] = np.arange(len(easy_data))

    # Set up the plot
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))  # 两个子图的画布

    # Define a function to plot data
    def plot_data(ax, scenario_data, title):
        for i in range(1, len(scenario_data)):
            # Get the conditions and indices for the current and previous points
            condition = scenario_data.iloc[i, scenario_data.columns.get_loc('scenario')]
            idx_prev = scenario_data.iloc[i-1, scenario_data.columns.get_loc('row_index')]
            idx_curr = scenario_data.iloc[i, scenario_data.columns.get_loc('row_index')]

            # Determine the color based on condition
            line_color = 'red' if condition == 'hard' else 'green'

            # Draw a line segment between the two points
            ax.plot([idx_prev, idx_curr], 
                    [scenario_data.iloc[i-1, scenario_data.columns.get_loc('Steering_Angle_Std')], 
                    scenario_data.iloc[i, scenario_data.columns.get_loc('Steering_Angle_Std')]],
                    color=line_color, marker='o')

        # Customize the plot
        ax.set_title(title)
        ax.set_xlabel('Row Index')
        ax.set_ylabel('Steering Angle Std')
        ax.plot([], [], color='red', label='hard')
        ax.plot([], [], color='green', label='easy')
        ax.legend(title='Condition')

    # Plot for each scenario
    plot_data(ax1, hard_data, 'Steering Angle Std Variation Over Time in Silence Condition')
    plot_data(ax2, easy_data, 'Steering Angle Std Variation Over Time in Hard Condition')

    # Set a common title
    fig.suptitle(file_name)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to make room for the common title
    plt.savefig(f'{subject}_result.png')