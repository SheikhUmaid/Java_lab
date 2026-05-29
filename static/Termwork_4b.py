# Decision Tree using ID3 Algorithm from Scratch

import pandas as pd
import math

# Load Dataset

data = pd.read_csv("play_tennis.csv")

# Function to calculate entropy

def entropy(data):
    target = data.iloc[:, -1]
    values = target.unique()

    ent = 0

    for value in values:
        probability = len(target[target == value]) / len(target)
        ent -= probability * math.log2(probability)

    return ent

# Function to calculate Information Gain

def information_gain(data, attribute):

    total_entropy = entropy(data)

    values = data[attribute].unique()

    weighted_entropy = 0

    for value in values:
        subset = data[data[attribute] == value]
        probability = len(subset) / len(data)
        weighted_entropy += probability * entropy(subset)

    gain = total_entropy - weighted_entropy

    return gain

# ID3 Algorithm

def id3(data, attributes):

    target = data.iloc[:, -1]

    # If all target values are same
    if len(target.unique()) == 1:
        return target.unique()[0]

    # If no attributes left
    if len(attributes) == 0:
        return target.mode()[0]

    # Select best attribute
    gains = [information_gain(data, attr) for attr in attributes]

    best_attribute = attributes[gains.index(max(gains))]

    tree = {best_attribute: {}}

    for value in data[best_attribute].unique():

        subset = data[data[best_attribute] == value]

        remaining_attributes = [attr for attr in attributes if attr != best_attribute]

        subtree = id3(subset, remaining_attributes)

        tree[best_attribute][value] = subtree

    return tree

attributes = list(data.columns[:-1])

decision_tree = id3(data, attributes)

print("Decision Tree using ID3 Algorithm:")
print(decision_tree)