import pandas as pd

# Load the datasets
feedback_data = pd.read_csv(r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\feedback\C02\with_subs\C02_Control_D01.csv')
silence_data = pd.read_csv(r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\silence\silence\C02_Control_D01.csv')

# Calculate the maximum meanDiam for each sub in the silence data
max_silence_diam = silence_data.groupby('sub')['meanDiam'].max()

# Map the maximum values to the feedback data using the 'sub' column
feedback_data['maxDiam'] = feedback_data['sub'].map(max_silence_diam)

# Subtract the mapped maximum values from the meanDiam in feedback data to create a new column
feedback_data['adjusted_meanDiam'] = feedback_data['meanDiam'] - feedback_data['maxDiam']

# Remove the temporary column
adjusted_feedback_data = feedback_data.drop(columns=['maxDiam'])

# Save the adjusted dataset to a new CSV file
adjusted_feedback_data.to_csv(r'D:\pupil-size-master\code\Examples\Dataset_nfb1\Results\modulation\C02_Control_D01_max.csv', index=False)
