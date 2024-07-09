import random

# Define the subjects
subjects = list(range(1, 11))

# Shuffle the subjects to ensure randomness
random.shuffle(subjects)

# Split the subjects into two groups
feedback_group = subjects[:5]
sham_group = subjects[5:]

# Print the group assignments
print("Feedback Group:", feedback_group)
print("Sham Group:", sham_group)
