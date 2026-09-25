# Problem Statement & System Specifications

## 1. Problem Statement
Standard Tic-Tac-Toe implementations are constrained to a static 3x3 grid with a fixed win threshold of 3 consecutive marks. This limited configuration suffers from small state-space complexity, leading to frequent draws and predictable game trees. The goal of this project is to implement an arbitrary-dimension $N \times N$ matrix game ($N \ge 3$) where the victory condition dynamically scales to $N$ consecutive marks along any row, column, or diagonal, coupled with single-player heuristics against an automated agent.

## 2. Objectives
* Build an interactive, extensible terminal-based Tic-Tac-Toe engine in Python.
* Implement dynamic matrix sizing ($N \times N$) based on runtime user configuration.
* Dynamically bind the win condition to $N$ marks in a row.
* Provide an automated opponent with selectable difficulty behaviors (random vs. best-move evaluation).
* Ensure strict boundary checking, turn alternating, and error handling for user inputs.

## 3. Scope & Constraints
* **Scope:** Command-line terminal interface, 2D array board representation, single-player vs AI mode.
* **Constraints:** Minimum grid size $N \ge 3$; input must be positive integers within valid index bounds $[0, N-1]$.
