# ♟️ Python Chess Game

## What It Is
A two-player chess game with a full graphical board, playable either against a friend or against a built-in AI opponent. Click a piece, click where you want it to go, and the game enforces every rule of chess along the way — including the tricky ones like castling and en passant.

## Technologies Involved
- **Python**. The language the entire project is written in
- **Pygame**. Handles the graphics: drawing the board, pieces, animations, and reading mouse/keyboard input

## Features
- Full legal move validation (no illegal moves possible)
- Castling, en passant, and pawn promotion
- Check, checkmate, and stalemate detection
- Move highlighting — click a piece to see every square it can legally move to
- Animated piece movement
- Move log panel showing the game's move history
- Undo (`Z`) and restart (`R`) shortcuts
- AI opponent that evaluates positions and thinks several moves ahead, rather than moving randomly

## Process
The project is split into three parts that each handle one job:
1. **The rules engine** — tracks the board and generates every legal move for each piece type
2. **The interface** — a loop that draws the board/pieces and turns mouse clicks into moves
3. **The AI** — scores possible positions (based on piece values and positioning) and searches a few moves ahead using a minimax-style algorithm with alpha-beta pruning to cut down on unnecessary searching

## What I Learned
- How to represent a chessboard and its rules in code, including edge cases like en passant and castling that are easy to overlook
- How search algorithms like minimax/negamax work, and how alpha-beta pruning speeds them up
- How to build an interactive graphical application with Pygame, including handling real-time input and animation
- How to structure a project into separate, single-responsibility files

## How It Can Be Improved
- Increase the AI's search depth for stronger play (currently limited to keep move times reasonable)
- Add move ordering to make alpha-beta pruning more effective
- Add a difficulty selector for the AI
- Support online multiplayer
- Add sound effects and a cleaner UI/theme options

## Running the Project
1. Install Python: [python.org/downloads](https://www.python.org/downloads/)
2. Install Pygame:
   ```
   pip install pygame
   ```
3. Keep `ChessMain.py`, `ChessEngine.py`, `ChessAI.py`, and an `images/` folder (with the piece images) in the same directory.
4. Run:
   ```
   python ChessMain.py
   ```

## Demo Video
<img src="UntitledProject-ezgif.com-crop_3.gif" width="600" alt="Chess AI Demo">


---
⭐️ A project by [Fernand Mata](https://github.com/matafn09)
