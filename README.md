2D Maze Game
------------------
------------------

🎮 Game Title: 2D Maze Game
📁 File: maze_game.py
📦 Dependencies:
- Python 3.x
- Pygame (pip install pygame)

------------------
------------------

🚀 How to Run the Game:
1. Make sure Python 3 is installed on your system.
2. Install Pygame by running:
   pip install pygame
3. Save the script as maze_game.py
4. Open terminal or command prompt in the directory containing the script.
5. Run the game:
   python maze_game.py

------------------
------------------

🕹️ Game Controls:
- Arrow Keys: Move the player (🔼 Up, 🔽 Down, ◀️ Left, ▶️ Right)
- R Key: Restart the game after winning
- Q Key: Quit the game

------------------
------------------

🎯 Objective:
Navigate the red player circle through the randomly generated maze to reach the green goal cell in the fewest moves and shortest time possible.

------------------
------------------

📊 Game Stats:
- Your move count and elapsed time are displayed during gameplay.
- Upon reaching the goal, your results are saved in a file named:
  maze_game_results.txt
  Each entry logs the date/time, number of moves, and total time taken.

------------------
------------------

🧠 How It Works:
- The maze is generated using a Recursive Backtracking Algorithm.
- Each maze is different every time the game restarts.
- The player can only move if no wall blocks the chosen direction.

------------------
------------------

📌 Notes:
- The maze is always solvable.
- All progress resets upon restarting.
- You can find saved results in the same folder as the script.
------------------
------------------

Developed by: Muhammad Shameer Asim

Enjoy solving the maze! 🧩
