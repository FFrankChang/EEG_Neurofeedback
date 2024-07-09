import random

# Generate middle conditions with equal silence and feedback
middle_conditions = ['silence'] * 5 + ['feedback'] * 5
random.shuffle(middle_conditions)

# Add silence to the first and last positions
conditions = ['silence'] + middle_conditions + ['silence']

# Print the experiment order and conditions
for i, condition in enumerate(conditions):
    print(f"Experiment {i+1}: {condition}")
