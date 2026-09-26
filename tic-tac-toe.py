import math
import random

# Tic-Tac-Toe game project.
# This program supports different board sizes and lets two players play against each other
# or play against the computer. The code is split into small functions so each part of
# the game is easier to understand and manage.

# This function prints the board on the screen.
# It converts the internal 2D list into a visible table that the player can understand.
def print_board(board):                   
    '''This generates a board of size NxN'''
    n = len(board)
    print("  " + " ".join(f" {c} " for c in range(n)))    #This is done in between the columns 
    for r in range(n):
        row_str = "|".join(f" {board[r][c]} " for c in range(n))
        print(f"{r} {row_str}")
        if r < n - 1:
            print("  " + "+".join(["---"] * n))           #This is joined with + in the between the rows


# This function checks whether anyone has won.
# It inspects rows, columns, and diagonals to find a full line of Xs or Os.
# If no one wins and the board is full, it returns Draw.
def check_winner(board): 
    '''This module checks who wins....'''
    n = len(board)

    # Check Rows
    for r in range(n):
        first = board[r][0]
        if first != " " and all(board[r][c] == first for c in range(n)):
            return first

    # Check Columns
    for c in range(n):
        first = board[0][c]
        if first != " " and all(board[r][c] == first for r in range(n)):
            return first

    # Check Main Diagonal
    first_main = board[0][0]
    if first_main != " " and all(board[i][i] == first_main for i in range(n)):
        return first_main

    # Check Anti-Diagonal
    first_anti = board[0][n - 1]
    if first_anti != " " and all(board[i][n - 1 - i] == first_anti for i in range(n)):
        return first_anti

    # Check for Draw or Ongoing Game
    if any(board[r][c] == " " for r in range(n) for c in range(n)):
        return None
    return "Draw"


# This function gives a score to one line of the board.
# It helps the AI decide if a row or diagonal is strong or weak.
def evaluate_line(line, n):   #
    o_count = line.count("O")
    x_count = line.count("X")

    if o_count > 0 and x_count > 0:
        return 0

    if o_count > 0:
        return 10 ** (o_count)
    if x_count > 0:
        return -(10 ** (x_count))
    return 0


# This function checks the whole board and adds up all the line scores.
# The AI uses this to judge the overall position before making a move.
def evaluate_board(board):
    n = len(board)
    score = 0

    for i in range(n):
        score += evaluate_line(board[i], n)
        score += evaluate_line([board[r][i] for r in range(n)], n)

    score += evaluate_line([board[i][i] for i in range(n)], n)
    score += evaluate_line([board[i][n - 1 - i] for i in range(n)], n)

    return score


# This function returns all empty cells on the board.
# These are the possible places where a player can move next.
def get_available_moves(board):
    n = len(board)
    return [(r, c) for r in range(n) for c in range(n) if board[r][c] == " "]


# This is the minimax algorithm.
# It looks ahead to future moves and decides which move gives the best result.
# The AI tries to maximize its chances of winning and minimize the opponent's chances.
def minimax(board, depth, is_maximizing, alpha, beta, max_depth):
    winner = check_winner(board)
    if winner == "O":
        return 1000000 - depth
    if winner == "X":
        return depth - 1000000
    if winner == "Draw":
        return 0
    if depth >= max_depth:
        return evaluate_board(board)

    moves = get_available_moves(board)

    if is_maximizing:
        max_eval = -math.inf
        for r, c in moves:
            board[r][c] = "O"
            ev = minimax(board, depth + 1, False, alpha, beta, max_depth)
            board[r][c] = " "
            max_eval = max(max_eval, ev)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for r, c in moves:
            board[r][c] = "X"
            ev = minimax(board, depth + 1, True, alpha, beta, max_depth)
            board[r][c] = " "
            min_eval = min(min_eval, ev)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval


# This function checks all legal moves and chooses the one with the best score.
# It is used by the computer to make smart decisions.
# At the hardest level, the AI first looks for immediate winning moves and blocks
# opponent wins so it is not only trying to draw.
def get_best_move(board):
    n = len(board)
    moves = get_available_moves(board)

    # First priority: win immediately if possible.
    for r, c in moves:
        board[r][c] = "O"
        if check_winner(board) == "O":
            board[r][c] = " "
            return (r, c)
        board[r][c] = " "

    # Second priority: block the opponent's immediate winning move.
    for r, c in moves:
        board[r][c] = "X"
        if check_winner(board) == "X":
            board[r][c] = " "
            return (r, c)
        board[r][c] = " "

    # If no immediate win or block is needed, do the deeper minimax search.
    max_depth = 6 if n == 3 else (4 if n == 4 else 3)
    best_val = -math.inf
    best_move = None

    center = (n - 1) / 2
    moves.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))

    for r, c in moves:
        board[r][c] = "O"
        move_val = minimax(board, 0, False, -math.inf, math.inf, max_depth)
        board[r][c] = " "
        if move_val > best_val:
            best_val = move_val
            best_move = (r, c)
    return best_move


# This function decides how the computer moves based on the difficulty selected by the player.
# Easy mode picks random moves, while harder modes use the minimax strategy.
def get_computer_move(board, difficulty):
    moves = get_available_moves(board)
    if difficulty == 1:
        return random.choice(moves)
    if difficulty == 2:
        return get_best_move(board) if random.random() < 0.5 else random.choice(moves)
    return get_best_move(board)


# This function takes input from the human player.
# It validates the row and column, checks whether the square is empty,
# and lets the player quit the game if needed.
def get_human_move(player, n, board):
    while True:
        user_input = input(
            f"\nPlayer {player}'s turn! Enter row and col (0 to {n-1}, e.g., '1 2' or 'q' to quit): "
        ).strip().lower()

        if user_input in ("q", "quit", "exit"):
            return None, None

        try:
            parts = user_input.split()
            if len(parts) != 2:
                print("Please enter exactly two numbers (row and column) or 'q' to exit.")
                continue
            r, c = int(parts[0]), int(parts[1])
            if not (0 <= r < n and 0 <= c < n):
                print(f"Coordinates out of bounds! Choose values between 0 and {n-1}.")
            elif board[r][c] != " ":
                print(f"Square ({r}, {c}) is already occupied! Pick an empty cell.")
            else:
                return r, c
        except ValueError:
            print("Invalid input. Please enter numbers only (e.g., '1 2') or 'q' to quit.")


# This function asks the user which mode they want to play.
# The player can choose between a two-player match or a match against the computer.
def select_game_mode():
    while True:
        print("\nSelect Game Mode:")
        print("  [1] Two Players (Human vs Human)")
        print("  [2] Single Player (Human vs AI)")

        choice = input("Enter mode choice (1 or 2): ").strip()
        if choice not in ("1", "2"):
            print("Invalid selection. Please enter 1 or 2.")
            continue

        selected_mode = int(choice)
        mode_label = (
            "Two Players (Human vs Human)"
            if selected_mode == 1
            else "Single Player (Human vs AI)"
        )

        confirm = input(
            f"You selected [{selected_mode}] {mode_label}. Confirm? (y to proceed / c to change): "
        ).strip().lower()
        if confirm in ("y", "yes"):
            return selected_mode
        elif confirm in ("c", "change"):
            print("Resetting choice. Please pick your game mode again.")
        else:
            print("Unrecognized response. Let's reselect.")


# This function runs one full round of the game.
# It sets up the board, chooses the mode, takes turns, checks for a winner,
# and ends the round when the match is over.
# The starting player alternates after each round so the second player gets the first move next time.
def play_round(starting_player="X"):
    print("=" * 50)
    print("           N x N CLASSIC TIC-TAC-TOE")
    print("=" * 50)

    # 1. Select Board Size
    while True:
        try:
            n = int(input("\nEnter board size N (e.g., 3 for 3x3, 4 for 4x4): ").strip())
            if n >= 3:
                break
            print("Please enter a board size of 3 or higher.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print(f"\nRule: Fill an entire line of {n} marks (row, col, or diagonal) to win.")
    print("Note: You can type 'q' at any turn to exit the current match.")

    # 2. Select Game Mode with confirmation & change option
    game_mode = select_game_mode()

    # 3. Select Difficulty (Only if playing against AI)
    difficulty = None
    if game_mode == 2:
        print("\nChoose AI Difficulty Level:")
        print("  [1] Easy   - Makes purely random moves")
        print("  [2] Medium - Plays a balanced mix of smart and casual moves")
        print("  [3] Hard   - Tactical Minimax AI")

        difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
        while True:
            diff_choice = input("Enter choice (1, 2, or 3): ").strip()
            if diff_choice in ("1", "2", "3"):
                difficulty = int(diff_choice)
                break
            print("Invalid selection. Please enter 1, 2, or 3.")

    board = [[" " for _ in range(n)] for _ in range(n)]
    current_player = starting_player

    if game_mode == 1:
        print(f"\nStarting Human vs Human game on a {n}x{n} grid!")
        print(f"This round starts with Player {starting_player} ('{starting_player}').")
        print("Player 1 is 'X', Player 2 is 'O'.\n")
    else:
        print(
            f"\nStarting Human vs AI game on a {n}x{n} grid! (Difficulty: {difficulty_labels[difficulty]})"
        )
        if starting_player == "O":
            print("The AI gets the first move in this round.\n")
        else:
            print("You get the first move in this round.\n")

    print_board(board)

    # Gameplay Loop
    while True:
        if current_player == "X":
            r, c = get_human_move("X", n, board)
            if r is None:
                print("\nMatch aborted by player.")
                break
            board[r][c] = "X"
        else:
            if game_mode == 1:
                r, c = get_human_move("O", n, board)
                if r is None:
                    print("\nMatch aborted by player.")
                    break
                board[r][c] = "O"
            else:
                print("\nComputer (O) is calculating its move...")
                r, c = get_computer_move(board, difficulty)
                board[r][c] = "O"
                print(f"Computer placed an 'O' at row {r}, column {c}.")

        print()
        print_board(board)

        winner = check_winner(board)
        if winner:
            print("\n" + "-" * 40)
            if winner == "Draw":
                print("Game Over: It's a draw! Well played.")
            elif winner == "X":
                if game_mode == 1:
                    print("Game Over: Player X wins!")
                else:
                    print("Congratulations! You defeated the AI!")
            else:
                if game_mode == 1:
                    print("Game Over: Player O wins!")
                else:
                    print("Game Over: The computer wins! Better luck next time.")
            print("-" * 40)
            break

        current_player = "O" if current_player == "X" else "X"


# This is the main function of the program.
# It starts the game and keeps asking the player whether they want to play again.
# The starting player alternates each round so the second player gets the first move next time.
def main():
    print("          Welcome to N x N Tic-Tac-Toe!")
    next_starter = "X"
    while True:
        play_round(starting_player=next_starter)
        if next_starter == "X":
            next_starter = "O"
        else:
            next_starter = "X"

        while True:
            play_again = (
                input("\nWould you like to play another round? (y/n): ")
                .strip()
                .lower()
            )
            if play_again in ("y", "yes"):
                print("\nRestarting game...\n")
                break
            elif play_again in ("n", "no"):
                print("\nThank you for playing! Have a great day!")
                return
            else:
                print("Please type 'y' for yes or 'n' for no.")


if __name__ == "__main__":
    main()
