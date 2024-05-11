import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

# 定义文件路径
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

plt.figure(figsize=(12, 6))
differences = raw_data['arousal'] - processed_data['mean_arousal']
plt.plot(combined_data['timestamp'],differences)
# plt.plot(combined_data['timestamp'], combined_data['arousal'], label='Raw Arousal')
# plt.plot(combined_data['timestamp'], combined_data['mean_arousal'], label='Processed Mean Arousal', linestyle='--', alpha=0.5)
plt.legend()
plt.title('Arousal Data Comparison')
plt.xlabel('Timestamp')
plt.ylabel('Arousal Value')
plt.show()
