import math
import random


def print_board(board):
    n = len(board)
    print("  " + " ".join(f" {c} " for c in range(n)))
    for r in range(n):
        row_str = "|".join(f" {board[r][c]} " for c in range(n))
        print(f"{r} {row_str}")
        if r < n - 1:
            print("  " + "+".join(["---"] * n))


def check_winner(board):
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


def evaluate_line(line, n):
    o_count = line.count("O")
    x_count = line.count("X")

    if o_count > 0 and x_count > 0:
        return 0

    if o_count > 0:
        return 10 ** (o_count)
    if x_count > 0:
        return -(10 ** (x_count))
    return 0


def evaluate_board(board):
    n = len(board)
    score = 0

    for i in range(n):
        score += evaluate_line(board[i], n)
        score += evaluate_line([board[r][i] for r in range(n)], n)

    score += evaluate_line([board[i][i] for i in range(n)], n)
    score += evaluate_line([board[i][n - 1 - i] for i in range(n)], n)

    return score


def get_available_moves(board):
    n = len(board)
    return [(r, c) for r in range(n) for c in range(n) if board[r][c] == " "]


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


def get_best_move(board):
    n = len(board)
    max_depth = 6 if n == 3 else (4 if n == 4 else 3)
    best_val = -math.inf
    best_move = None
    moves = get_available_moves(board)

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


def get_computer_move(board, difficulty):
    moves = get_available_moves(board)
    if difficulty == 1:
        return random.choice(moves)
    if difficulty == 2:
        return get_best_move(board) if random.random() < 0.5 else random.choice(moves)
    return get_best_move(board)


def get_human_move(player, n, board):
    while True:
        user_input = input(
            f"\nPlayer {player}'s turn! Enter row and col (0 to {n-1}, e.g., '1 2'): "
        ).strip()
        try:
            parts = user_input.split()
            if len(parts) != 2:
                print("Please enter exactly two numbers (row and column).")
                continue
            r, c = int(parts[0]), int(parts[1])
            if not (0 <= r < n and 0 <= c < n):
                print(f"Coordinates out of bounds! Choose values between 0 and {n-1}.")
            elif board[r][c] != " ":
                print(f"Square ({r}, {c}) is already occupied! Pick an empty cell.")
            else:
                return r, c
        except ValueError:
            print("Invalid input. Please enter numbers only (e.g., '1 2').")


def play_round():
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

    # 2. Select Game Mode (PvP or PvAI)
    print("\nSelect Game Mode:")
    print("  [1] Two Players (Human vs Human)")
    print("  [2] Single Player (Human vs AI)")

    while True:
        mode_choice = input("Enter mode choice (1 or 2): ").strip()
        if mode_choice in ("1", "2"):
            game_mode = int(mode_choice)
            break
        print("Invalid selection. Please enter 1 or 2.")

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
    current_player = "X"

    if game_mode == 1:
        print(f"\nStarting Human vs Human game on a {n}x{n} grid!")
        print("Player 1 is 'X', Player 2 is 'O'.\n")
    else:
        print(f"\nStarting Human vs AI game on a {n}x{n} grid! (Difficulty: {difficulty_labels[difficulty]})")
        print("You are 'X', AI is 'O'.\n")

    print_board(board)

    # Gameplay Loop
    while True:
        if current_player == "X":
            r, c = get_human_move("X", n, board)
            board[r][c] = "X"
        else:
            if game_mode == 1:
                r, c = get_human_move("O", n, board)
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


def main():
    print("Welcome to N x N Tic-Tac-Toe!")
    while True:
        play_round()
        while True:
            play_again = input("\nWould you like to play another round? (y/n): ").strip().lower()
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
    
