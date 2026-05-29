import numpy as np

x = np.array([1,2,3,4,5], dtype=float)
y = np.array([2,4,5,4,5], dtype=float)

m = 0
c = 0
learning_rate = 0.01
iterations = 1000
n = len(x)

for _ in range(iterations):
    y_pred = m * x + c

    dm = (-2/n) * np.sum(x * (y - y_pred))
    dc = (-2/n) * np.sum(y - y_pred)

    m = m - learning_rate * dm
    c = c - learning_rate * dc

print("Slope:", m)
print("Intercept:", c)

prediction = m * 6 + c
print("Prediction:", prediction)