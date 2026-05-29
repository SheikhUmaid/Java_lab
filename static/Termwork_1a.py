# Tic-Tac-Toe using Brute Force Strategy

board = [' ' for _ in range(9)]


def display_board():
    print()
    for i in range(3):
        print(board[i * 3], '|', board[i * 3 + 1], '|', board[i * 3 + 2])
        if i < 2:
            print('--+---+--')
    print()


def check_winner(player):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for pos in win_positions:
        if all(board[i] == player for i in pos):
            return True
    return False


def is_draw():
    return ' ' not in board


def human_move():
    while True:
        pos = int(input("Enter position (1-9): ")) - 1
        if 0 <= pos <= 8 and board[pos] == ' ':
            board[pos] = 'X'
            break
        else:
            print("Invalid move! Try again.")


def computer_move():
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            break


while True:
    display_board()
    human_move()

    if check_winner('X'):
        display_board()
        print("Human Player Wins!")
        break

    if is_draw():
        display_board()
        print("Game Draw!")
        break

    computer_move()

    if check_winner('O'):
        display_board()
        print("Computer Wins!")
        break

    if is_draw():
        display_board()
        print("Game Draw!")
        break