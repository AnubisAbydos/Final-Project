"""
Project Name: BoardGame
File Name: main.py
Author: Lex Hall
Last Updated: 7/29/19
Python Version: 3.6
"""
import os

import game

def main():
    # Set console size (Only confirmed for Windows OS)
    os.system("mode con cols=100 lines=50")
    mainGame = game.Game()
    mainGame.play()

if __name__ == "__main__":
    main()