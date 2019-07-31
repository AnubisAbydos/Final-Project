"""
Project Name: BoardGame
File Name: tile.py
Author: Lex Hall
Last Updated: 7/29/19
Python Version: 3.6
"""

from enums import *

class Tile(object):
    def __init__(self):
        self.color = TeamColor.NONE
        self.troopCount = 0
        self.isBase = False
        self.isCaptured = False
        self.isResearch = False
        self.isVictoryPoint = False

    ### Sets game starting base conditions
    def setBase(self, color):
        self.color = color
        self.isBase = True
        self.troopCount = 5

    def setCapturedBase(self, color):
        self.color = color
        self.isCaptured = True
        self.troopCount = 0

    def addTroops(self, troopsToAdd, color):
            self.color = color
            if self.troopCount + troopsToAdd <= 25:
                self.troopCount += troopsToAdd

    def removeTroops(self, troopsToRemove):
        if self.troopCount >= troopsToRemove:
            self.troopCount -= troopsToRemove
        if self.troopCount == 0 and not self.isBase:
            self.color = TeamColor.NONE

    ### Handles the attrition of each tile awarding research or victory as required
    def applyAttrition(self, player):
        if self.troopCount > 0:
            self.removeTroops(1)
            if self.color == player.color:
                if self.isResearch:
                    player.takeResearchCard()
                else:
                    player.victoryPoints += 1

    ### Used for printing board
    def printColor(self):
        if self.color == TeamColor.NONE:
            print("        ", end = "")
        else:
            print('{:^8s}'.format(self.color.name), end = "")

    ### Used for printing board
    def printSoldier(self):
        if self.color == TeamColor.NONE:
            print("        ", end = "")
        else:
            print('{:^8d}'.format(self.troopCount), end = "")

    ### Used for printing board
    def printSpecial(self):
        if self.isResearch:
            print('{:^8s}'.format("RESEARCH"), end = "")
        elif self.isVictoryPoint:
            print('{:^8s}'.format("VICTORY"), end = "")
        elif self.isBase:
            print('{:^8s}'.format("BASE"), end = "")
        else:
            print("        ", end = "")

    ### Used for printing board
    def printTile(self, isBottom, isRight):
        if self.color == TeamColor.NONE:
            for i in range(8):
                if not isRight:
                    print("        |")
                else:
                    print("        ")

        else:
            for i in range(2):
                if not isRight:
                    print("        |")
                else:
                    print("        ")
            
            
            if self.isBase:
                print('{:^8s}'.format("BASE"))
                for i in range(2):
                    if not isRight:
                        print("        |")
                    else:
                        print("        ")
            else:
                for i in range(3):
                    if not isRight:
                        print("        |")
                    else:
                        print("        ")
        if not isBottom and not isRight:
            print("________|")
        elif not isBottom and isRight:
            print("________")