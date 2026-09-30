import math
import random

# N x N Tic-Tac-Toe project
# Supports custom grid sizes and both 2-player and AI gameplay modes.


def print_board(board):
    n = len(board)
    # Print column header indices
    print("  " + " ".join(f" {c} " for c in range(n)))
    for r in range(n):
        row_str = "|".join(f" {board[r][c]} " for c in range(n))
        print(f"{r} {row_str}")
        if r < n - 1:
            print("  " + "+".join(["---"] * n))


def check_winner(board):
    n = len(board)

    # Check rows
    for r in range(n):
        if board[r][0] != " " and all(board[r][c] == board[r][0] for c in range(n)):
            return board[r][0]

    # Check columns
    for c in range(n):
        if board[0][c] != " " and all(board[r][c] == board[0][c] for r in range(n)):
            return board[0][c]

    # Check main diagonal
    if board[0][0] != " " and all(board[i][i] == board[0][0] for i in range(n)):
        return board[0][0]

    # Check anti-diagonal
    if board[0][n - 1] != " " and all(board[i][n - 1 - i] == board[0][n - 1] for i in range(n)):
        return board[0][n - 1]

    # Check for empty spots or draw
    for r in range(n):
        for c in range(n):
            if board[r][c] == " ":
                return None
    return "Draw"


# Score heuristic for individual rows, cols, or diagonals
def evaluate_line(line, n):
    o_count = line.count("O")
    x_count = line.count("X")

    # If both marks exist in the same line, neither can complete it
    if o_count > 0 and x_count > 0:
        return 0

    if o_count > 0:
        return 10 ** o_count
    if x_count > 0:
        return -(10 ** x_count)
    return 0


# Sum heuristic scores across the entire board
def evaluate_board(board):
    n = len(board)
    total_score = 0

    for i in range(n):
        # Rows and columns
        total_score += evaluate_line(board[i], n)
        total_score += evaluate_line([board[r][i] for r in range(n)], n)

    # Both diagonals
    total_score += evaluate_line([board[i][i] for i in range(n)], n)
    total_score += evaluate_line([board[i][n - 1 - i] for i in range(n)], n)

    return total_score


# Get list of open coordinates
def get_available_moves(board):
    n = len(board)
    moves = []
    for r in range(n):
        for c in range(n):
            if board[r][c] == " ":
                moves.append((r, c))
    return moves


# Minimax search with alpha-beta pruning and dynamic depth cutoff
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
        best_val = -math.inf
        for r, c in moves:
            board[r][c] = "O"
            score = minimax(board, depth + 1, False, alpha, beta, max_depth)
            board[r][c] = " "
            best_val = max(best_val, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_val
    else:
        best_val = math.inf
        for r, c in moves:
            board[r][c] = "X"
            score = minimax(board, depth + 1, True, alpha, beta, max_depth)
            board[r][c] = " "
            best_val = min(best_val, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_val


# Select best tactical move for the AI
def get_best_move(board):
    n = len(board)
    moves = get_available_moves(board)

    # 1. Take immediate win if available
    for r, c in moves:
        board[r][c] = "O"
        if check_winner(board) == "O":
            board[r][c] = " "
            return (r, c)
        board[r][c] = " "

    # 2. Block opponent's immediate win
    for r, c in moves:
        board[r][c] = "X"
        if check_winner(board) == "X":
            board[r][c] = " "
            return (r, c)
        board[r][c] = " "

    # Depth limits based on board size to avoid slow execution
    max_depth = 6 if n == 3 else (4 if n == 4 else 3)
    best_score = -math.inf
    best_move = None

    # Move ordering: center-outward heuristic
    center = (n - 1) / 2
    moves.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))

    for r, c in moves:
        board[r][c] = "O"
        score = minimax(board, 0, False, -math.inf, math.inf, max_depth)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move


# Pick move based on active difficulty level
def get_computer_move(board, difficulty):
    moves = get_available_moves(board)
    if difficulty == 1:
        return random.choice(moves)
    if difficulty == 2:
        return get_best_move(board) if random.random() < 0.5 else random.choice(moves)
    return get_best_move(board)


# Prompt and validate human player move
def get_human_move(player, n, board):
    while True:
        user_input = input(
            f"\nPlayer {player}'s turn! Enter row and col (0 to {n-1}, e.g., '1 2' or 'q' to quit): "
        ).strip().lower()

        if user_input in ("q", "quit", "exit"):
            return None, None

        parts = user_input.split()
        if len(parts) != 2:
            print("Please enter exactly two numbers (row and column) or 'q' to exit.")
            continue

        try:
            r, c = int(parts[0]), int(parts[1])
            if not (0 <= r < n and 0 <= c < n):
                print(f"Coordinates out of bounds! Choose values between 0 and {n-1}.")
            elif board[r][c] != " ":
                print(f"Square ({r}, {c}) is already occupied! Pick an empty cell.")
            else:
                return r, c
        except ValueError:
            print("Invalid input. Please enter numbers only (e.g., '1 2') or 'q' to quit.")


# Select 2-player or single-player mode
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


# Main game loop for a single round
def play_round(starting_player="X"):
    print("=" * 50)
    print("           N x N CLASSIC TIC-TAC-TOE")
    print("=" * 50)

    # 1. Select board size
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

    # 2. Select game mode
    game_mode = select_game_mode()

    # 3. Select AI difficulty if applicable
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

    # Turn loop
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


def start_game():
    print("          Welcome to N x N Tic-Tac-Toe!")
    next_starter = "X"
    while True:
        play_round(starting_player=next_starter)
        # Alternate starter for each consecutive round
        next_starter = "O" if next_starter == "X" else "X"

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
    start_game()
