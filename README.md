# Snakes and Ladders Game

Video Demo: https://youtu.be/VLkwi4Bx_9o

## Description

**Snakes and Ladders** is a Python implementation of the classic board game. The game can be played by two players or by one player against the computer.

The main objective is simple: the first player to reach tile **100** wins the game. During the game, players roll the dice and move across the board. Some tiles contain special effects that can move the player forward or backward.

Instead of using real snake and ladder images, the game uses colored tiles:

* 🔵 **Blue** – Positive effect, similar to a ladder.
* 🔴 **Red** – Negative effect, similar to a snake.
* ⚪ **Gray** – Normal tile.

The game board is generated randomly, which makes every new round different.

## How to Run

### Requirements

* Python 3
* Tkinter
* SQLite3

The libraries used in this project are included with Python, so no additional packages are required.

To run the project:

1. Download the project.
2. Open a terminal inside the project folder.
3. Run:

```bash
python project.py
```

## How to Play

1. Start the game.
2. Choose the number of players.
3. If playing against the computer, choose the computer difficulty level.
4. Press the dice button to roll the dice.
5. The player moves according to the dice result.
6. Special tiles can move the player forward or backward.
7. The first player to reach tile **100** wins.

## Features

The game includes:

* A board with 100 tiles.
* Randomly generated positive and negative effects.
* Two-player mode.
* Player versus computer mode.
* Three computer difficulty levels.
* Smooth player movement animations.
* Dice rolling system.
* Current player position display.
* Round counter.
* Win counter for both players.
* Restart button.
* Settings menu.
* Custom player colors.
* Winner screen.
* SQLite database for saving game settings.

## Computer Difficulty

The computer has three difficulty levels.

### Level 1

The computer rolls the dice randomly, similar to a normal player.

### Level 2

The computer checks possible moves and tries to avoid negative tiles.

### Level 3

The computer tries to choose positive tiles, avoid negative tiles, and select safe positions when possible.

## Main Functions

The project uses several important functions:

* `new_map()` – Creates a new game map with random effects.
* `chaing()` – Handles the dice roll and player movement logic.
* `pons()` – Moves the player with a smooth animation.
* `click()` – Handles the main dice button and player turns.
* `computer_turn()` – Controls the computer player's turn.
* `re_zero()` – Resets the players and starts a new round.
* `winer()` – Detects and displays the winner.
* `start_game()` – Applies the selected settings and starts the game.
* `new_map_block()` – Creates the graphical game board.
* `update_map()` – Updates the board using the generated map.
* `check_num_chaing()` – Calculates the player's new position.
* `check_name_chaing()` – Determines the player name when players share a tile.
* `check_color_chaing()` – Determines the color of special tiles.

## Settings

The settings window allows the player to change:

* Number of players.
* Computer difficulty.
* Player 1 color.
* Player 2 color.

The selected settings are saved using an **SQLite database**, so they can be used again when the program is restarted.

## Testing

The project includes tests using **Pytest**.

The tests check important game logic, including:

* Player position calculations.
* Player names when two players are on the same tile.
* Positive and negative tile colors.

The tested functions are:

* `check_num_chaing()`
* `check_name_chaing()`
* `check_color_chaing()`

## Technologies Used

This project was built using:

* **Python** – Main programming language.
* **Tkinter** – Graphical user interface.
* **SQLite3** – Saving game settings.
* **Random** – Dice rolls and random map generation.
* **Pytest** – Testing important game functions.

## Future Improvements

Possible improvements for future versions include:

* Adding real snake and ladder graphics.
* Adding sound effects and music.
* Improving the computer AI.
* Supporting more players.
* Adding online multiplayer using a server.
* Adding more board designs and themes.
* Improving the animation system.

## Conclusion

This project combines several Python concepts, including graphical user interfaces, game logic, animations, databases, random generation, and testing.

The goal of the project was to create a simple but enjoyable version of the classic **Snakes and Ladders** game while adding custom features such as randomly generated effects, computer difficulty levels, saved settings, and smooth player movement.
