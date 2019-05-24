"""
Project Name: 
File Name: main.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

import game
import os

def main():
    os.system("mode con cols=100 lines=50")
    mainGame = game.Game()
    mainGame.play()

if __name__ == "__main__":
    main()