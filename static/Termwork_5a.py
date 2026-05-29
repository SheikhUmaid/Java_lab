import heapq


def manhattan(state, goal):
    distance = 0

    for i in range(1, 9):
        x1, y1 = divmod(state.index(i), 3)
        x2, y2 = divmod(goal.index(i), 3)
        distance += abs(x1 - x2) + abs(y1 - y2)

    return distance


def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    x, y = divmod(index, 3)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:
            new_index = nx * 3 + ny
            temp = list(state)
            temp[index], temp[new_index] = temp[new_index], temp[index]
            neighbors.append(tuple(temp))

    return neighbors


def a_star(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set()

    while pq:
        cost, state, path = heapq.heappop(pq)

        if state == goal:
            print("Solution Path:")
            for step in path + [state]:
                print(step)
            return

        if state in visited:
            continue

        visited.add(state)

        for neighbor in get_neighbors(state):
            heapq.heappush(
                pq,
                (
                    len(path) + 1 + manhattan(neighbor, goal),
                    neighbor,
                    path + [state]
                )
            )


start = (1,2,3,4,0,5,6,7,8)
goal = (1,2,3,4,5,6,7,8,0)

a_star(start, goal)