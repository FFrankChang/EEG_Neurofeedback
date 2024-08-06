import pandas as pd

def filter_data(source_file, column_to_select, group=None, condition=None):
    # Load the data
    data = pd.read_csv('results.csv')
    if group:
        filtered_data = data[(data['Group'] == group) & data['Source_File'].str.contains(source_file)]
        grouped_data = filtered_data.groupby('Condition')[column_to_select].apply(list).to_dict()
    elif condition:
        filtered_data = data[(data['Condition'] == condition) & (data['Source_File'] == source_file)]
        grouped_data = filtered_data.groupby('Group')[column_to_select].apply(list).to_dict()
    else:
        grouped_data = None
    
    return grouped_data

def filter_data_2(source_file, column_to_select, condition=None):
    # Load the data
    data = pd.read_csv('results.csv')
    
    filtered_data = data[(data['Condition'] == condition) & (data['Source_File'] == source_file)]
    grouped_data = filtered_data.groupby('Group')[column_to_select].apply(list).to_dict()

    return grouped_data

# Example usage:
source_file = '40'
column_to_select = 'Min_TTC'

grouped_by_condition = filter_data(source_file, column_to_select, group='Sham')
for i in grouped_by_condition:
    print(grouped_by_condition[i])

# grouped_by_group = filter_data(source_file, column_to_select, condition='feedback')
# print(grouped_by_group)

# a= filter_data_2(source_file,column_to_select,condition='feedback')
# print(a)
