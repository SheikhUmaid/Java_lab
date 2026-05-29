from collections import deque

capacity_a = 4
capacity_b = 3
goal = 2


def bfs():
    visited = set()
    queue = deque([((0, 0), [(0, 0)])])

    while queue:
        (x, y), path = queue.popleft()

        if y == goal:
            print("Solution Path:")
            for state in path:
                print(state)
            return

        next_states = [
            (capacity_a, y),
            (x, capacity_b),
            (0, y),
            (x, 0),
            (x - min(x, capacity_b - y), y + min(x, capacity_b - y)),
            (x + min(y, capacity_a - x), y - min(y, capacity_a - x))
        ]

        for state in next_states:
            if state not in visited:
                visited.add(state)
                queue.append((state, path + [state]))


bfs()