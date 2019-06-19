"""
Project Name: 
File Name: enums.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

import tile
from enums import *

class Board(object):
    def __init__(self):
        # row(left A-J) by column(top 1-10)
        self.boardGrid = [[0 for i in range(10)] for j in range(10)]
        # load boardGrid
        for i in range(10):
            for j in range(10):
                self.boardGrid[i][j] = tile.Tile()
        # Set Special Tiles
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
        self.boardGrid[4][4].setVictoryPoint()
        self.boardGrid[5][5].setVictoryPoint()
        # Research Points (Center)
        self.boardGrid[4][5].setResearch()
        self.boardGrid[5][4].setResearch()

    # TODO Remove all Getters and Setters (replace with properities)
    def getBoardGrid(self):
        return self.boardGrid

    def applyAttrition(self, player):
        self.boardGrid[4][4].applyAttrition(player)
        self.boardGrid[5][5].applyAttrition(player)
        self.boardGrid[4][5].applyAttrition(player)
        self.boardGrid[5][4].applyAttrition(player)

    def baseCapture(self, transferFrom, transferTo):
        for i in range(10):
            for j in range(10):
                if self.boardGrid[i][j].getTeamColor() == transferFrom:
                    if self.boardGrid[i][j].getIsBase():
                        self.boardGrid[i][j].setCapturedBase(transferTo)
                    else:
                        self.boardGrid[i][j].removeTroops(self.boardGrid[i][j].getTroopCount())
    
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
