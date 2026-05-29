from collections import deque

capacity_a = 4
capacity_b = 3
goal = 2

visited = set()


def dfs(state, path):
    x, y = state

    if y == goal:
        print("Solution Path:")
        for p in path:
            print(p)
        return True

    visited.add(state)

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
            if dfs(state, path + [state]):
                return True

    return False


start = (0, 0)
dfs(start, [start])