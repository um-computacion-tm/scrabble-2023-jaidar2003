# Scrabble

The aim of this development initiative is to create a Scrabble game using the Python programming language, following the rules and principles outlined in the Wikipedia entry on the game. 
The resulting game will allow users to participate in Scrabble matches via a text-based interface and will include functions for the game board, 
letter tiles, scoring and word validity checking.

# RULES

Scrabble rules:
                        
1. Aim of the game: The aim of Scrabble is to form words on a game board using letters with assigned values to obtain the highest possible score.
                        
2. The board: The Scrabble board is a square of 15x15 squares. Some squares have special values and bonuses.
                        
3. Tiles: The game is played with tiles representing letters. Each tile has a numerical value that determines its score. 
The number of tiles and their value vary according to the language you are playing in.
                        
4. Start of the game: Each player takes 7 tiles at random from the set of tiles, which are replenished after each play.
                        
5. Words: Players must form words on the board using their counters. Words must be formed from left to right or top to bottom, 
and must be connected to at least one letter already on the board.
                        
6. Scoring: Each letter has a numerical value assigned to it. The score of a word is the sum of the letter values in that word. In addition, the board has bonus squares, the board has bonus squares that can double or triple the score of a word or a letter.
                        
7. Shifting tiles: A player may choose to shift some or all of his tiles on his turn, but this costs him a full turn.
                        
8. End of the game: The game ends when all the tiles have been used up and a player has used all his tiles or when no more valid moves can be made.
                        
9. Winner: The player with the highest score at the end of the game wins.
                        
10. Valid words: Words must be valid words in the language you are using, and can be consulted in an official dictionary if a dispute arises.

"""

## Current Status

| *_CircleCI_* | *_Main branch_* |
| :---:   | :---:   |
| Status |[![CircleCI](https://dl.circleci.com/status-badge/img/gh/um-computacion-tm/scrabble-2023-jaidar2003/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/um-computacion-tm/scrabble-2023-jaidar2003/tree/main)

| _*Codeclimate*_ | *_Coverage_* | *_Maintainability_* |
| :---:   | :---:   | :---: |
| Status |[![Test Coverage](https://api.codeclimate.com/v1/badges/73676511189bdd7736c5/test_coverage)](https://codeclimate.com/github/um-computacion-tm/scrabble-2023-jaidar2003/test_coverage) | [![Maintainability](https://api.codeclimate.com/v1/badges/73676511189bdd7736c5/maintainability)](https://codeclimate.com/github/um-computacion-tm/scrabble-2023-jaidar2003/maintainability)

# Download
```bash
git clone https://github.com/um-computacion-tm/scrabble-2023-jaidar2003
```

# How To Run Scrabble In Docker

1. Make sure to have docker installed. You can install Docker from Docker oficial web site (https://www.docker.com/get-started) if you dont have it. 

2. Install Git using in cmd: -apt-get install git-

3. Clone the repository using: -git clone git@github.com:um-computacion-tm/scrabble-2023-jaidar2003.git
4. Navigate to the repository directory: cd /.../scrabble-2023-jaidar2003.git

5. Build the Docker image: -docker build -t image_name .-  (In image name give it the name you want)

6. Run the Docker image: -docker run -it image_name-

# Disclaimer

When I wrote this code, only Allah and I knew how it worked,
now only Allah knows it

Thereforce if yu are trying to optimize the routine and it fails (most surely), please 
increse the counter as a warning to the next person:

total_hours_here = 254

# Student Data

Universidad De Mendoza

Computacion I

Juan Manuel Aidar "62005" 

2023


