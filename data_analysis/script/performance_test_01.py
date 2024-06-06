import pandas as pd
import matplotlib.pyplot as plt


file_path = r'E:\EEG_Neurofeedback\sj_results.csv' 
test_data = pd.read_csv(file_path)

hard_data = test_data[test_data['scenario'] == 'hard']
# hard_data = test_data

mean_change_rates = hard_data.filter(regex='Coefficient of Variation \d')

reshaped_data = mean_change_rates.stack().reset_index(drop=True)

plt.figure(figsize=(12, 6))
plt.plot(reshaped_data, marker='o', linestyle='-',color='slateblue')
plt.title('Sequential Coefficient of Variation  for "Hard" Scenario')
plt.xlabel('Data Point Index')
plt.ylabel('Mean Change Rate')
plt.grid(True)
plt.show()
