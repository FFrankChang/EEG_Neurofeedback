import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

raw_data_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\data\\psd_20240512_163902_final.csv'
processed_data_path = 'D:\\Frank_Project\\EEG_Neurofeedback\\test3.csv'

raw_data = pd.read_csv(raw_data_path)
processed_data = pd.read_csv(processed_data_path)

combined_data = pd.merge_asof(raw_data.sort_index(), processed_data.sort_index(), on='timestamp', direction='nearest')
# combined_data.to_csv('a.csv',index=False)

correlation_coefficient = np.corrcoef(combined_data['arousal'], combined_data['arousal_pl'])[0, 1]
print(f"相关系数: {correlation_coefficient}")

mse = mean_squared_error(combined_data['arousal'], combined_data['arousal_pl'])
print(f"均方误差: {mse}")

differences = raw_data['arousal'] - processed_data['arousal_pl']

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(combined_data['timestamp'], combined_data['arousal'], label='Raw Arousal')
ax1.plot(combined_data['timestamp'], combined_data['arousal_pl'], label='Processed Mean Arousal', linestyle='--', alpha=0.5)
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Arousal Value')
ax1.legend(loc='upper left')  

# ax2 = ax1.twinx()  
# ax2.plot(combined_data['timestamp'], differences, label='Difference', color='lightcoral',linewidth=0.5)
# ax2.set_ylabel('Difference in Arousal')
# ax2.legend(loc='upper right') 

plt.title('Arousal Data Comparison')

# Display the plot
plt.show()