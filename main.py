"""
Title: Minesweeper
Author: Chris Blangiardi
Start Date: 7/25/2023

Description:
A simple game of minesweeper. The game should abide by the normal rules of minesweeper.
"""

import generate_board


def main():
    game = generate_board.Minesweeper()
    game.play()


if __name__ == "__main__":
    main()

