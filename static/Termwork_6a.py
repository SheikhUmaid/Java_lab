import heapq


def manhattan(state, goal):
    distance = 0

    for i in range(1, 9):
        x1, y1 = divmod(state.index(i), 3)
        x2, y2 = divmod(goal.index(i), 3)
        distance += abs(x1 - x2) + abs(y1 - y2)

    return distance


def neighbors(state):
    result = []
    idx = state.index(0)
    x, y = divmod(idx, 3)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:
            new_idx = nx * 3 + ny
            temp = list(state)
            temp[idx], temp[new_idx] = temp[new_idx], temp[idx]
            result.append(tuple(temp))

    return result


def greedy_best_first(start, goal):
    pq = []
    heapq.heappush(pq, (manhattan(start, goal), start, []))
    visited = set()

    while pq:
        _, state, path = heapq.heappop(pq)

        if state == goal:
            print("Solution Path:")
            for step in path + [state]:
                print(step)
            return

        if state in visited:
            continue

        visited.add(state)

        for n in neighbors(state):
            heapq.heappush(pq, (manhattan(n, goal), n, path + [state]))


start = (1,2,3,4,0,5,6,7,8)
goal = (1,2,3,4,5,6,7,8,0)

greedy_best_first(start, goal)