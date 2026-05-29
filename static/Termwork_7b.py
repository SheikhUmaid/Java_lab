import numpy as np


X = np.array([
    [1,2],
    [1.5,1.8],
    [5,8],
    [8,8],
    [1,0.6],
    [9,11]
])

k = 2

centroids = X[:k]

for _ in range(10):

    clusters = [[] for _ in range(k)]

    for point in X:
        distances = [np.linalg.norm(point - centroid) for centroid in centroids]
        cluster_index = np.argmin(distances)
        clusters[cluster_index].append(point)

    new_centroids = []

    for cluster in clusters:
        new_centroids.append(np.mean(cluster, axis=0))

    centroids = np.array(new_centroids)

print("Final Centroids:")
print(centroids)