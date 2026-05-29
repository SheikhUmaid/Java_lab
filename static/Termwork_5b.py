# Naive Bayes Algorithm from Scratch

import pandas as pd

# Load Dataset

data = pd.read_csv("play_tennis.csv")

# Calculate Prior Probabilities

total_rows = len(data)

play_yes = data[data['PlayTennis'] == 'Yes']
play_no = data[data['PlayTennis'] == 'No']

prior_yes = len(play_yes) / total_rows
prior_no = len(play_no) / total_rows

# Test Sample

test_data = {
    'Outlook': 'Sunny',
    'Temperature': 'Cool',
    'Humidity': 'High',
    'Wind': 'Strong'
}

# Function to calculate likelihood

def likelihood(feature, value, target_data):

    count = len(target_data[target_data[feature] == value])
    total = len(target_data)

    return count / total

# Calculate Posterior Probability for Yes

prob_yes = prior_yes

for feature, value in test_data.items():
    prob_yes *= likelihood(feature, value, play_yes)

# Calculate Posterior Probability for No

prob_no = prior_no

for feature, value in test_data.items():
    prob_no *= likelihood(feature, value, play_no)

print("Probability of Yes:", prob_yes)
print("Probability of No:", prob_no)

# Prediction

if prob_yes > prob_no:
    print("Prediction: Play Tennis = Yes")
else:
    print("Prediction: Play Tennis = No")