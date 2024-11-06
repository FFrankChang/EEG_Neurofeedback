import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

top_folder = r'G:\Exp_V0_data\data'

output_folder = r'G:\Exp_V0_data\steer_plot'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for folder in os.listdir(top_folder):
    if folder.startswith('S') and os.path.isdir(os.path.join(top_folder, folder)):
        # 找到包含C04的CSV文件
        csv_files = glob.glob(os.path.join(top_folder, folder, '*C04*.csv'))
        
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df['event_triggered'] = df['event_triggered'].astype(bool)
            event_indices = df[df['event_triggered']].index
            line_color = 'lightcoral' if 'traffic' in csv_file.lower() else 'royalblue'

            nrows = (len(event_indices) + 3) // 4
            fig, axes = plt.subplots(nrows=nrows, ncols=4, figsize=(20, 5 * nrows), constrained_layout=True)
            axes = axes.flatten()
            
            for i in range(len(event_indices) - 1):
                start_idx = event_indices[i]
                end_idx = event_indices[i + 1] - 1
                start_time = df.loc[start_idx, 'timestamp']
                df['time_since_event_start'] = (df['timestamp'] - start_time) 
                
                axes[i].plot(df.loc[start_idx:end_idx, 'time_since_event_start'], df.loc[start_idx:end_idx, 'steer_angle'],c=line_color)
                axes[i].set_title(f'Event: {i}')
                axes[i].set_xlabel('Time (s)')
                axes[i].set_ylabel('Steer Angle')
                axes[i].grid(True)

            for j in range(i + 1, len(axes)):
                axes[j].axis('off')

            fig.suptitle(os.path.basename(csv_file))
            
            png_filename = os.path.join(output_folder, os.path.basename(csv_file).replace('.csv', '.png'))
            plt.savefig(png_filename)
            plt.close(fig)  
