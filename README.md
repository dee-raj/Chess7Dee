
# Chess Game Using Python

![Chess Game Logo](app-logo.ico)

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The "Chess Game Using Python" project is a console-based chess game developed in Python. It provides a user-friendly interface for playing chess against another player or a computer opponent. The game includes features such as player vs. player, player vs. AI, customizable timers, and a clear display of game results.

## Features

- **Player vs. Player:** Enjoy a classic game of chess with a friend or family member locally on the same device.
- **Player vs. AI:** Challenge yourself against an AI opponent using the Mini-Max algorithm for strategic gameplay.
- **Customizable Timers:** Add an extra layer of strategy with customizable timers for each player's turn.
- **User-Friendly Interface:** The graphical user interface (GUI) provides an intuitive and visually appealing experience.
- **Offline Gameplay:** Play the game without the need for an internet connection.
- **Learning Opportunity:** Use the game as a tool for learning and improving chess skills.

## Getting Started

### Prerequisites

Before running the Chess Game, make sure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3)
- [Git](https://git-scm.com/downloads)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (usually included with Python installations)
- [Pygame](https://www.pygame.org/wiki/GettingStarted) (install using `pip install pygame`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dee-raj/Chess7Dee
   ```

2. Navigate to the project directory:

   ```bash
   cd Chess7Dee
   ```

3. Run the main Python file to start the game:

   ```bash
   python HomeScreen.py
   ```

## Usage

- Choose the game mode (Player vs. Player, Player vs. AI) from the main menu.
- Make your moves by selecting the piece and the destination square.
- Enjoy the game!

## Project Structure

The project has the following structure:

```
Chess7Dee
│
└-> __pycache__
   -> ChessAI.cpython-311.pyc
   -> ChessEngine.cpython-311.pyc
│
│-> app-logo.ico
├-> images
│  -> bB.png
│  -> bK.png
│  -> bN.png
│  -> bp.png
│  -> bQ.png
│  -> bR.png
│  -> wB.png
│  -> wK.png
│  -> wN.png
│  -> wp.png
│  -> wQ.png
│  -> wR.png
│
│-> ChessAI.py
│-> ChessEngine.py
│-> HomeScreen.py
│-> .gitignore
```

- **.gitignore**: Specifies files and directories to be ignored by Git.
- **app-logo.ico**: Icon file for the application.
- **ChessAI.py**: Code for the AI opponent.
- **ChessEngine.py**: Main logic of the chess game.
- **HomeScreen.py**: Display the home screen of the game.
- **main.py**: Main Python file to run the game.
- **images**: Directory containing image files used in the game.
- **__pycache__**: Directory containing Python cache files.

## Contributing

If you'd like to contribute to the project, please follow the [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
