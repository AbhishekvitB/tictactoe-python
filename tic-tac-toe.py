import math
import random

WIN_COUNT = 3


def print_board(board):
    n = len(board)
    print("  " + " ".join(f" {c} " for c in range(n)))
    for r in range(n):
        row_str = "|".join(f" {board[r][c]} " for c in range(n))
        print(f"{r} {row_str}")
        if r < n - 1:
            print("  " + "+".join(["---"] * n))


def check_line(line):
    count_x = 0
    count_o = 0
    for cell in line:
        if cell == "X":
            count_x += 1
            count_o = 0
            if count_x == WIN_COUNT:
                return "X"
        elif cell == "O":
            count_o += 1
            count_x = 0
            if count_o == WIN_COUNT:
                return "O"
        else:
            count_x = 0
            count_o = 0
    return None


def check_winner(board):
    n = len(board)
    k = WIN_COUNT

    # Rows
    for r in range(n):
        winner = check_line(board[r])
        if winner:
            return winner

    # Columns
    for c in range(n):
        col_cells = [board[r][c] for r in range(n)]
        winner = check_line(col_cells)
        if winner:
            return winner

    # Main diagonals
    for start_r in range(n):
        for start_c in range(n):
            if start_r + k <= n and start_c + k <= n:
                diag = [board[start_r + i][start_c + i] for i in range(k)]
                if all(cell == diag[0] and cell != " " for cell in diag):
                    return diag[0]

    # Anti-diagonals
    for start_r in range(n):
        for start_c in range(n):
            if start_r + k <= n and start_c - k + 1 >= 0:
                diag = [board[start_r + i][start_c - i] for i in range(k)]
                if all(cell == diag[0] and cell != " " for cell in diag):
                    return diag[0]

    # Draw or ongoing
    if any(board[r][c] == " " for r in range(n) for c in range(n)):
        return None
    return "Draw"


def evaluate_window(window):
    score = 0
    o_count = window.count("O")
    x_count = window.count("X")
    empty_count = window.count(" ")

    if o_count == 3:
        score += 100
    elif o_count == 2 and empty_count == 1:
        score += 10
    elif o_count == 1 and empty_count == 2:
        score += 1

    if x_count == 3:
        score -= 100
    elif x_count == 2 and empty_count == 1:
        score -= 15
    elif x_count == 1 and empty_count == 2:
        score -= 1

    return score


def evaluate_board(board):
    n = len(board)
    k = WIN_COUNT
    score = 0

    for r in range(n):
        for c in range(n - k + 1):
            score += evaluate_window([board[r][c + i] for i in range(k)])

    for c in range(n):
        for r in range(n - k + 1):
            score += evaluate_window([board[r + i][c] for i in range(k)])

    for r in range(n - k + 1):
        for c in range(n - k + 1):
            score += evaluate_window([board[r + i][c + i] for i in range(k)])

    for r in range(n - k + 1):
        for c in range(k - 1, n):
            score += evaluate_window([board[r + i][c - i] for i in range(k)])

    return score


def get_available_moves(board):
    n = len(board)
    return [(r, c) for r in range(n) for c in range(n) if board[r][c] == " "]


def minimax(board, depth, is_maximizing, alpha, beta, max_depth):
    winner = check_winner(board)
    if winner == "O":
        return 1000 - depth
    if winner == "X":
        return depth - 1000
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


def play_round():
    while True:
        try:
            n = int(input("Enter board dimension N (e.g., 3, 4, 5, 6): ").strip())
            if n >= 3:
                break
            print("Board size must be at least 3.")
        except ValueError:
            print("Please enter a valid integer.")
    WIN_COUNT=n
    print(f"\nGoal: Connect {WIN_COUNT} in a row to win.\n")
    
    print("\nSelect Difficulty:")
    print("1. Easy (Random)")
    print("2. Medium (Mixed)")
    print("3. Hard (Alpha-Beta Minimax)")

    while True:
        choice = input("Enter difficulty (1, 2, or 3): ").strip()
        if choice in ("1", "2", "3"):
            difficulty = int(choice)
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    board = [[" " for _ in range(n)] for _ in range(n)]
    current_player = "X"

    print()
    print_board(board)

    while True:
        if current_player == "X":
            while True:
                user_input = input(
                    f"\nPlayer X, enter row and col (0-{n-1}, e.g., '1 2'): "
                ).strip()
                try:
                    r, c = map(int, user_input.split())
                    if 0 <= r < n and 0 <= c < n and board[r][c] == " ":
                        board[r][c] = "X"
                        break
                    else:
                        print(f"Spot taken or out of range (0-{n-1}). Try again.")
                except ValueError:
                    print(
                        "Invalid input format. Enter two numbers separated by a space."
                    )
        else:
            print("\nComputer (O) is thinking...")
            r, c = get_computer_move(board, difficulty)
            board[r][c] = "O"

        print_board(board)

        winner = check_winner(board)
        if winner:
            if winner == "Draw":
                print("\nIt's a draw!")
            else:
                print(f"\nPlayer {winner} wins!")
            break

        current_player = "O" if current_player == "X" else "X"


def main():
    while True:
        play_round()
        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ("y", "yes"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
