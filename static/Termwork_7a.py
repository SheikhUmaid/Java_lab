N = 9


def print_board(board):
    for row in board:
        print(row)


def is_safe(board, row, col, num):

    for x in range(N):
        if board[row][x] == num:
            return False

    for x in range(N):
        if board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def solve(board, row, col):

    if row == N - 1 and col == N:
        return True

    if col == N:
        row += 1
        col = 0

    if board[row][col] > 0:
        return solve(board, row, col + 1)

    for num in range(1, N + 1):

        if is_safe(board, row, col, num):
            board[row][col] = num

            if solve(board, row, col + 1):
                return True

        board[row][col] = 0

    return False


board = [
    [3,0,6,5,0,8,4,0,0],
    [5,2,0,0,0,0,0,0,0],
    [0,8,7,0,0,0,0,3,1],
    [0,0,3,0,1,0,0,8,0],
    [9,0,0,8,6,3,0,0,5],
    [0,5,0,0,9,0,6,0,0],
    [1,3,0,0,0,0,2,5,0],
    [0,0,0,0,0,0,0,7,4],
    [0,0,5,2,0,6,3,0,0]
]

if solve(board, 0, 0):
    print_board(board)
else:
    print("No solution exists")