import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    return data

def compute_differences(data):
    # Group by Subject and Day, and pivot to make 'Condition' a sublevel in columns
    grouped = data.groupby(['Subject', 'Day', 'Condition']).mean()
    pivot_data = grouped.unstack(level=-1)

    # Calculate the difference metrics: feedback - silence
    difference_metrics = pivot_data.xs('feedback', level='Condition', axis=1) - pivot_data.xs('silence', level='Condition', axis=1)
    return difference_metrics

def visualize_improvements(difference_metrics):
    # Melt the DataFrame to work with seaborn easily
    melted_df = difference_metrics.reset_index().melt(id_vars=['Subject', 'Day'], var_name='Metric', value_name='Difference')

    # Plot using seaborn
    plt.figure(figsize=(15, 10))
    sns.barplot(x='Metric', y='Difference', hue='Subject', data=melted_df)
    plt.title('Improvement in Metrics Under Feedback Condition')
    plt.axhline(0, color='red', linestyle='--')  # Add a line at y=0 for reference
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Specify the path to your data file
    file_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\grouped_expv1_c01_results_d.csv'

    # Load and prepare the data
    data = load_and_prepare_data(file_path)
    
    # Compute differences between conditions
    differences = compute_differences(data)
    
    # Visualize the improvements
    visualize_improvements(differences)

if __name__ == "__main__":
    main()
