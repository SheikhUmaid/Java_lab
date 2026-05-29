# Multiple Linear Regression using Gradient Descent
# House Price Prediction Dataset

import pandas as pd
import numpy as np

# Load Dataset

data = pd.read_csv("house_price.csv")

X = data[['Area', 'Bedrooms', 'Age']].values
Y = data['Price'].values

# Feature Scaling
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

m = len(Y)
n = X.shape[1]

# Initialize weights and bias
weights = np.zeros(n)
bias = 0

learning_rate = 0.01
iterations = 1000

# Gradient Descent
for i in range(iterations):

    predictions = np.dot(X, weights) + bias

    error = predictions - Y

    dw = (1/m) * np.dot(X.T, error)
    db = (1/m) * np.sum(error)

    weights = weights - learning_rate * dw
    bias = bias - learning_rate * db

# Final Parameters
print("Weights:", weights)
print("Bias:", bias)

# Prediction
new_house = np.array([[2400, 5, 3]])

# Apply same normalization
new_house = (new_house - np.mean(data[['Area', 'Bedrooms', 'Age']].values, axis=0)) / np.std(data[['Area', 'Bedrooms', 'Age']].values, axis=0)

predicted_price = np.dot(new_house, weights) + bias

print("Predicted House Price:", predicted_price[0])