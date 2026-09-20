
def display_board(board):
    #print board in terminal
    print(board[0][0], "|", board[0][1], "|", board[0][2])
    print("---------")
    print(board[1][0], "|", board[1][1], "|", board[1][2])
    print("---------")
    print(board[2][0], "|", board[2][1], "|", board[2][2])

def player_input(player):
    # get move from player
    row = int(input(f"player {player}, enter row (0, 1, or 2): "))
    col = int(input(f"player {player}, enter column (0, 1, or 2): "))
    return row, col

def check_winner(board, player):

    if board[0][0] == player and board[0][1] == player and board[0][2] == player:
        return True
    if board[1][0] == player and board[1][1] == player and board[1][2] == player:
        return True
    if board[2][0] == player and board[2][1] == player and board[2][2] == player:
        return True

    if board[0][0] == player and board[1][0] == player and board[2][0] == player:
        return True
    if board[0][1] == player and board[1][1] == player and board[2][1] == player:
        return True
    if board[0][2] == player and board[1][2] == player and board[2][2] == player:
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def check_tie(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play():
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    player = "X"

    while True:
        display_board(board)
        row, col = player_input(player)
        board[row][col] = player

        if check_winner(board, player):
            display_board(board)
            print(f"player {player} wins!")
            break
        if check_tie(board):
            display_board(board)
            print("its a tie!")
            break

        if player == "X":
            player = "O"
        else:
            player = "X"

play()
