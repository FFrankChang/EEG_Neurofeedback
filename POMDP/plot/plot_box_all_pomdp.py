import pandas as pd
import matplotlib.pyplot as plt
for i  in range(10,70,10):
    duration = i
    # Load the data
    file_path = rf'D:\gitee\EEG_Neurofeedback\POMDP\results\results_ex\final_results_{duration}s.csv'
    data = pd.read_csv(file_path)

    # Filter data where Condition is 'feedback'
    feedback_data = data[data['Condition'] == 'feedback']

    # Group data by 'Day'
    grouped = feedback_data.groupby('Day')

    # Columns to plot
    columns_to_plot = ['Min_TTC', 'Steering_Angle_STD', 'Acceleration_x_Mean', 'Acceleration_x_STD', 'Acceleration_x_Change_Rate_Mean', 'Road_Exits']

    # Create a figure with 2 rows and 3 columns for the subplots
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
    axes = axes.flatten()  # Flatten the array of axes to make indexing easier

    # Plot each column in a subplot
    for index, column in enumerate(columns_to_plot):
        data_to_plot = [group[column].tolist() for _, group in grouped]
        
        # Customizing boxplot styles
        whiskerprops = dict(linestyle='--', linewidth=1)
        capprops = dict(linestyle='-', linewidth=1)
        flierprops = dict(marker='o', markerfacecolor='black', markersize=2, linestyle='none')
        medianprops = dict(linestyle='-', linewidth=1, color='black')  # Ensure the median line is visible

        # Create the boxplot
        bplot = axes[index].boxplot(data_to_plot, labels=grouped.groups.keys(), whiskerprops=whiskerprops, capprops=capprops, flierprops=flierprops, medianprops=medianprops, patch_artist=False, widths=0.5)

        # Assign colors for specific group to the box lines
        for box, label in zip(bplot['boxes'], grouped.groups.keys()):
            box.set(color='blue' if label == 'D02' else 'black', linewidth=2)  # Change linewidth if needed

        axes[index].set_title(f'{column}')
        axes[index].set_xlabel('Trails')
        axes[index].set_ylabel(column)
        axes[index].grid(True)  # Add grid for better readability

    # Add an overall title
    fig.suptitle(f"Metrics for {duration}s", fontsize=16)

    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect parameter as needed

    # Save the figure
    plt.savefig(f'boxplots_{duration}s.png')
