import numpy as np

x = np.array([1,2,3,4,5])
y = np.array([2,4,5,4,5])

mean_x = np.mean(x)
mean_y = np.mean(y)

numerator = np.sum((x - mean_x) * (y - mean_y))
denominator = np.sum((x - mean_x) ** 2)

b1 = numerator / denominator
b0 = mean_y - b1 * mean_x

print("Slope:", b1)
print("Intercept:", b0)

x_test = 6
prediction = b0 + b1 * x_test

print("Prediction:", prediction)