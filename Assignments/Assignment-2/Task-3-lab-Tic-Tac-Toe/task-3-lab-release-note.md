# Task 3 - Lab - Tic-Tac-Toe

- Assignment: 2
- Task 3, Lab: Tic-Tac-Toe
- Name: Pattarapol Tantechasa
- Student ID: 103883220
- Email: [103883220@student.swin.edu.au](mailto:103883220@student.swin.edu.au)

## Release Note

- Designed software architecture for the game, final diagram can be found [HERE](./tic-tac-toe-diagram.png). Note that the first [diagram](./diagram.png) created just for starting point, it works well with CLI version but I update to final diagram just to align with Pygame version.
- Implemented Tic-Tac-Toe in pygame using OOP with a clear game loop trinity (`process_input`, `update_model`, `render`).
- Created two AI bots:
  - `RandomAI` — picks any empty cell at random.
  - `SmartAI` — uses Goal Oriented Behaviour, prioritising winning, then blocking, then random fallback.
- Both AIs print their decision reasoning to the terminal each move.
- AI vs AI mode is playable in pygame with a 600ms delay between moves so the game is visible.
- Press `R` to restart the game at any time.
- Code can be run by using terminal:
  - `cd` into `Task-3-lab-Tic-Tac-Toe/tic-tac-toe` folder.
  - Run `python main.py` command in terminal.
  - To change game mode (Human vs AI, AI vs AI), swap agents in `main.py`.
