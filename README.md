# N-in-a-Row Dynamic Tic-Tac-Toe

## Overview
A dynamic, customizable command-line implementation of the classic Tic-Tac-Toe game written in Python. Unlike traditional 3x3 setups, this application supports scalable board dimensions ($N \ge 3$) where the objective dynamically scales to match the board size—requiring players to connect $N$ consecutive marks (horizontally, vertically, or diagonally) to secure a win. The game features an interactive single-player mode with an AI opponent providing variable difficulty levels.

---

## Features
* **Dynamic Grid Sizing:** Configurable $N \times N$ board size ($3 \times 3$, $4 \times 4$, $5 \times 5$, etc.) with input validation.
* **Adaptive Win Conditions:** Target streak count dynamically binds to the chosen dimension $N$.
* **AI Opponent:** Integrated computer player featuring multiple difficulty settings and randomized heuristic evaluation.
* **Robust Input Sanitization:** Gracefully handles invalid grid inputs, out-of-bounds moves, and occupied cell attempts.
* **Terminal Interface:** Real-time visual grid rendering directly inside the terminal.

---

## Technologies / Tools Used
* **Language:** Python 3.8+
* **Standard Libraries:** `random`, `sys`
* **Development Environment:** Visual Studio Code

---

## Steps to Install & Run the Project

### Prerequisites
* Ensure Python 3 is installed. Verify via terminal:
  ```bash
  python --version
