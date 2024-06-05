import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the data from the CSV file
file_path = r'D:\gitee\EEG_Neurofeedback\aa.csv'
result_df = pd.read_csv(file_path)

# Calculate the absolute values for the coefficient of variation
result_df['silence_avg_coef_var'] = result_df['silence_avg_coef_var'].abs()
result_df['feedback_avg_coef_var'] = result_df['feedback_avg_coef_var'].abs()

# Plotting the comparison results
plt.figure(figsize=(12, 8))
x = np.arange(len(result_df))
width = 0.35

plt.bar(x - width/2, result_df['silence_avg_coef_var'], width, label='Silence', color='lightblue')
plt.bar(x + width/2, result_df['feedback_avg_coef_var'], width, label='Feedback', color='lightcoral')

plt.xlabel('Subject Name')
plt.ylabel('Absolute Average Coefficient of Variation')
plt.title('Comparison of Absolute Average Coefficient of Variation: Silence vs Feedback')
plt.xticks(x, result_df['subject_name'], rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
