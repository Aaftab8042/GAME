import tkinter as tk
from tkinter import messagebox
import random


def check_winner():
    """Check if there's a winner and highlight the winning combination."""
    for combo in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            for i in combo:
                buttons[i].config(bg="#FFD700", relief="sunken")
            display_winner(buttons[combo[0]]["text"])
            return True
    if all(button["text"] != "" for button in buttons):
        display_winner("None (Draw)")
        return True
    return False


def display_winner(winner):
    """Show the winner in a styled popup."""
    popup = tk.Toplevel(root)
    popup.title("Game Over")
    popup.geometry("350x250")
    popup.configure(bg="#4CAF50")

    label = tk.Label(
        popup,
        text=f"{'It\'s a draw!' if winner == 'None (Draw)' else f'Player {winner} Wins!'}",
        font=("Arial", 18, "bold"),
        bg="#4CAF50",
        fg="white",
        wraplength=300
    )
    label.pack(expand=True, fill=tk.BOTH)

    button = tk.Button(
        popup,
        text="Play Again",
        font=("Arial", 14, "bold"),
        bg="#FFD700",
        fg="black",
        activebackground="#FFD700",
        command=lambda: [popup.destroy(), reset_game()],
    )
    button.pack(pady=10)
    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)


def reset_game():
    """Reset the game board and UI."""
    global current_player
    current_player = "X"
    for button in buttons:
        button.config(text="", bg="#d3d3d3", relief="raised")
    label.config(text="Player X's turn")


def button_click(index):
    """Handle button clicks, update state, and manage AI moves."""
    if buttons[index]["text"] == "":
        buttons[index]["text"] = current_player
        if not check_winner():
            toggle_player()
            if game_mode == "1 vs Computer" and current_player == "O":
                root.after(500, computer_move)


def toggle_player():
    """Switch between X and O players."""
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")


def computer_move():
    """Computer's AI to make a move."""
    empty_buttons = [i for i in range(9) if buttons[i]["text"] == ""]
    if empty_buttons:
        if difficulty_level == 1:  # Easy level: Random moves
            index = random.choice(empty_buttons)
        elif difficulty_level == 2:  # Medium: Block opponent
            index = smarter_move(empty_buttons, block=True)
        else:  # Hard: Win, block, or play strategically
            index = smarter_move(empty_buttons)
        buttons[index]["text"] = "O"
    check_winner()
    toggle_player()


def smarter_move(empty_buttons, block=False):
    """AI to either block, win, or choose strategically."""
    for i in empty_buttons:
        buttons[i]["text"] = "O" if not block else "X"  # Attempt to win or block
        if check_winner():
            buttons[i]["text"] = ""  # Restore state
            return i
        buttons[i]["text"] = ""
    return random.choice(empty_buttons)


def start_game(mode, level=1):
    """Start the game with chosen mode and difficulty."""
    global game_mode, difficulty_level, current_player
    game_mode = mode
    difficulty_level = level
    current_player = "X"
    reset_game()
    mode_frame.pack_forget()
    if mode == "1 vs Computer":
        level_frame.pack_forget()
    game_frame.pack()


def show_level_page():
    """Show difficulty selection for '1 vs Computer'."""
    mode_frame.pack_forget()
    level_frame.pack()


root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

# Frames
mode_frame = tk.Frame(root, bg="#f0f0f0")
level_frame = tk.Frame(root, bg="#f0f0f0")
game_frame = tk.Frame(root, bg="#f0f0f0")

# Mode Selection
tk.Label(mode_frame, text="Select Game Mode", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

tk.Button(mode_frame, text="1 vs 1", font=("Arial", 16), width=12, command=lambda: start_game("1 vs 1"),
          bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(mode_frame, text="1 vs Computer", font=("Arial", 16), width=15, command=show_level_page,
          bg="#2196F3", fg="white").pack(pady=10)

# Difficulty Selection
tk.Label(level_frame, text="Select Difficulty (1-3)", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)
for i, difficulty in enumerate(["Easy", "Medium", "Hard"], 1):
    tk.Button(level_frame, text=difficulty, font=("Arial", 14), width=10,
              command=lambda lvl=i: start_game("1 vs Computer", lvl),
              bg="#FF9800", fg="white").pack(pady=10)

# Game Board
buttons = [tk.Button(game_frame, text="", font=("Arial", 25, "bold"), width=6, height=2,
                     bg="#d3d3d3", command=lambda i=i: button_click(i)) for i in range(9)]
for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
label = tk.Label(game_frame, text="Player X's turn", font=("Arial", 16), bg="#f0f0f0")
label.grid(row=3, column=0, columnspan=3)

mode_frame.pack()
root.mainloop()