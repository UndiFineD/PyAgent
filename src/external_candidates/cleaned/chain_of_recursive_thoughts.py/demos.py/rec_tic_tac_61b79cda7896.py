# Extracted from: C:\DEV\PyAgent\.external\Chain-of-Recursive-Thoughts\demos\rec-tic-tac.py
import random
import tkinter as tk
from tkinter import messagebox


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)


def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],  # rows
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],  # columns
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],  # diagonals
    ]
    return [player, player, player] in win_conditions


def check_draw(board):
    return all(cell != " " for row in board for cell in row)


def ai_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)


def on_button_click(row, col):
    global current_player
    if board[row][col] == " " and not game_over:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        if check_winner(board, current_player):
            messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
            disable_all_buttons()
        elif check_draw(board):
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            disable_all_buttons()
        else:
            current_player = "O" if current_player == "X" else "X"
            if current_player == "O" and single_player_mode:
                ai_row, ai_col = ai_move(board)
                board[ai_row][ai_col] = "O"
                buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
                if check_winner(board, "O"):
                    messagebox.showinfo("Tic Tac Toe", "Player O wins!")
                    disable_all_buttons()
                elif check_draw(board):
                    messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                    disable_all_buttons()
                else:
                    current_player = "X"


def disable_all_buttons():
    global game_over
    game_over = True
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)


def start_game(mode):
    global board, buttons, current_player, game_over, single_player_mode
    single_player_mode = mode == "single"
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    for row in buttons:
        for button in row:
            button.config(text=" ", state=tk.NORMAL)


def create_buttons(frame):
    global buttons
    buttons = []
    for i in range(3):
        button_row = []
        for j in range(3):
            button = tk.Button(
                frame,
                text=" ",
                font=("normal", 20, "normal"),
                width=5,
                height=2,
                command=lambda row=i, col=j: on_button_click(row, col),
            )
            button.grid(row=i, column=j)
            button_row.append(button)
        buttons.append(button_row)


def main():
    global root
    root = tk.Tk()
    root.title("Tic Tac Toe")

    mode_frame = tk.Frame(root)
    mode_frame.pack(pady=10)

    tk.Button(mode_frame, text="Single Player", command=lambda: start_game("single")).pack(side=tk.LEFT, padx=10)
    tk.Button(mode_frame, text="Multi Player", command=lambda: start_game("multi")).pack(side=tk.LEFT, padx=10)

    game_frame = tk.Frame(root)
    game_frame.pack()

    create_buttons(game_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
