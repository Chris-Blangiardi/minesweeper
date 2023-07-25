"""
Title: Minesweeper
Author: Chris Blangiardi
Start Date: 7/25/2023

Description:
A simple game of minesweeper. The game should abide by the normal rules of minesweeper.
"""

import board


def main():
    game = board.Minesweeper(1280, 720)
    game.play()


if __name__ == "__main__":
    main()

