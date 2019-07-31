"""
Project Name: BoardGame
File Name: board.py
Author: Lex Hall
Last Updated: 7/29/19
Python Version: 3.6
"""

import tile
from enums import *

''' CLASS Board
Contains the array of tiles that comprise the board itself.
'''
class Board(object):
    def __init__(self):
        # row(left A-J) by column(top 1-10)
        self.boardGrid = [[0 for i in range(10)] for j in range(10)]
        # load boardGrid
        for i in range(10):
            for j in range(10):
                self.boardGrid[i][j] = tile.Tile()
        # Set Special Rules Tiles
        # Red (Top)
        self.boardGrid[0][3].setBase(TeamColor.RED)
        self.boardGrid[0][4].setBase(TeamColor.RED)
        self.boardGrid[0][5].setBase(TeamColor.RED)
        self.boardGrid[0][6].setBase(TeamColor.RED)
        # Blue (Bottom)
        self.boardGrid[9][3].setBase(TeamColor.BLUE)
        self.boardGrid[9][4].setBase(TeamColor.BLUE)
        self.boardGrid[9][5].setBase(TeamColor.BLUE)
        self.boardGrid[9][6].setBase(TeamColor.BLUE)
        # Yellow (Right)
        self.boardGrid[3][9].setBase(TeamColor.YELLOW)
        self.boardGrid[4][9].setBase(TeamColor.YELLOW)
        self.boardGrid[5][9].setBase(TeamColor.YELLOW)
        self.boardGrid[6][9].setBase(TeamColor.YELLOW)
        # Green (Left)
        self.boardGrid[3][0].setBase(TeamColor.GREEN)
        self.boardGrid[4][0].setBase(TeamColor.GREEN)
        self.boardGrid[5][0].setBase(TeamColor.GREEN)
        self.boardGrid[6][0].setBase(TeamColor.GREEN)
        # Victory Points (Center)
        self.boardGrid[4][4].isVictoryPoint = True
        self.boardGrid[5][5].isVictoryPoint = True
        # Research Points (Center)
        self.boardGrid[4][5].isResearch = True
        self.boardGrid[5][4].isResearch = True

    ### Calls each of the center tiles Attrition function passing the turns current player
    def applyAttrition(self, player):
        self.boardGrid[4][4].applyAttrition(player)
        self.boardGrid[5][5].applyAttrition(player)
        self.boardGrid[4][5].applyAttrition(player)
        self.boardGrid[5][4].applyAttrition(player)

    # TODO Add check for home base or captured base and capture only captured or all bases
    def baseCapture(self, transferFrom, transferTo):
        for i in range(10):
            for j in range(10):
                if self.boardGrid[i][j].color == transferFrom:
                    if self.boardGrid[i][j].isBase:
                        self.boardGrid[i][j].setCapturedBase(transferTo)
                    else:
                        self.boardGrid[i][j].removeTroops(self.boardGrid[i][j].troopCount)
    
    def displayBoard(self):
        row = 0
        rowLetter = RowAlpha.A
        nextColorLine = 0
        nextSoldierLine = 1
        nextSpecialLine = 2
        nextEndLine = 3
        print ("      1        2        3        4        5        6        7        8        9        10    ")
        print ("  +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+")
        for i in range(39):
            if i == nextColorLine:
                print("  +", end = "")
                for j in range(10):
                    self.boardGrid[row][j].printColor()
                    if j != 9:
                        print("|", end = "")
                    else:
                        print("+")
                nextColorLine += 4
            elif i == nextSoldierLine:
                print("{:1s} +".format(rowLetter.name), end = "")
                if rowLetter.value != 9:
                    rowLetter = RowAlpha(rowLetter.value + 1)
                for j in range(10):
                    self.boardGrid[row][j].printSoldier()
                    if j != 9:
                        print("|", end = "")
                    else:
                        print("+")
                nextSoldierLine += 4
            elif i == nextSpecialLine:
                print("  +", end = "")
                for j in range(10):
                    self.boardGrid[row][j].printSpecial()
                    if j != 9:
                        print("|", end = "")
                    else:
                        print("+")
                nextSpecialLine += 4
                row += 1
            elif i == nextEndLine:
                print("  +-----------------------------------------------------------------------------------------+")
                nextEndLine += 4
            else:
                print("  +        |        |        |        |        |        |        |        |        |        +")
        print ("  +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+", end = "\n\n")
