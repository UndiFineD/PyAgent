# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_tic_tac_3173a44a82a7.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_tic_tac.py

# Extracted from: C:\DEV\PyAgent\.external\Chain-of-Recursive-Thoughts\demos\tic-tac.py

# NOTE: extracted with static-only rules; review before use


def print_board(board):
    print("-------------")

    for row in board:
        print("| " + " | ".join(row) + " |")

        print("-------------")


def check_winner(board, player):
    # Check rows, columns, and diagonals for a winner

    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True

        if all([board[j][i] == player for j in range(3)]):
            return True

    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False


def is_board_full(board):
    return all([cell != " " for row in board for cell in row])


def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]

    current_player = "X"

    while True:
        print_board(board)

        row = int(input(f"Player {current_player}, enter the row (0, 1, 2): "))

        col = int(input(f"Player {current_player}, enter the column (0, 1, 2): "))

        if board[row][col] != " ":
            print("This spot is already taken. Try again.")

            continue

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)

            print(f"Player {current_player} wins!")

            break

        if is_board_full(board):
            print_board(board)

            print("It's a tie!")

            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    tic_tac_toe()
