import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

raw_data_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\data\\20240430_01_final_02\\psd_20240430_152635_final.csv'
processed_data_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\processed_arousal_values.csv'

raw_data = pd.read_csv(raw_data_path)
processed_data = pd.read_csv(processed_data_path)

combined_data = pd.merge_asof(raw_data.sort_index(), processed_data.sort_index(), on='timestamp', direction='nearest')
# combined_data.to_csv('a.csv',index=False)

correlation_coefficient = np.corrcoef(combined_data['arousal'], combined_data['mean_arousal'])[0, 1]
print(f"相关系数: {correlation_coefficient}")

mse = mean_squared_error(combined_data['arousal'], combined_data['mean_arousal'])
print(f"均方误差: {mse}")

differences = raw_data['arousal'] - processed_data['mean_arousal']

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting 'arousal' and 'mean_arousal' on the first y-axis
ax1.plot(combined_data['timestamp'], combined_data['arousal'], label='Raw Arousal')
ax1.plot(combined_data['timestamp'], combined_data['mean_arousal'], label='Processed Mean Arousal', linestyle='--', alpha=0.5)
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Arousal Value')
ax1.legend(loc='upper left')  # Place legend in the upper left of the plot

# Create a second y-axis for 'differences'
ax2 = ax1.twinx()  
ax2.plot(combined_data['timestamp'], differences, label='Difference', color='lightcoral',linewidth=0.5)
ax2.set_ylabel('Difference in Arousal')

# Adding a legend to the second axis
ax2.legend(loc='upper right')  # Place legend in the upper right of the plot

# Adding a title
plt.title('Arousal Data Comparison')

# Display the plot
plt.show()