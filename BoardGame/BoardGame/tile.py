"""
Project Name: 
File Name: tile.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

from enums import *

class Tile(object):
    def __init__(self):
        # TODO Add Captured base property and change base capture to only take the captured base or all bases.
        self.color = TeamColor.NONE
        self.troopCount = 0
        self.isBase = False
        self.isResearch = False
        self.isVictoryPoint = False

    # TODO Remove all Getters and Setters (replace with properities)
    def getTeamColor(self):
        return self.color

    def getIsBase(self):
        return self.isBase

    def getTroopCount(self):
        return self.troopCount

    def setBase(self, color):
        self.color = color
        self.isBase = True
        self.troopCount = 5

    def setCapturedBase(self, color):
        self.color = color
        self.troopCount = 0

    def setResearch(self):
        self.isResearch = True

    def setVictoryPoint(self):
        self.isVictoryPoint = True

    def addTroops(self, troopsToAdd, color):
            self.color = color
            if self.troopCount + troopsToAdd <= 25:
                self.troopCount += troopsToAdd

    def removeTroops(self, troopsToRemove):
        if self.troopCount >= troopsToRemove:
            self.troopCount -= troopsToRemove
        if self.troopCount == 0 and not self.isBase:
            self.color = TeamColor.NONE

    def applyAttrition(self, player):
        if self.troopCount > 0:
            self.removeTroops(1)
            if self.color == player.getTeamColor():
                if self.isResearch:
                    player.takeResearchCard()
                else:
                    player.gainCommandPoints(1)

    def printColor(self):
        if self.color == TeamColor.NONE:
            print("        ", end = "")
        else:
            print('{:^8s}'.format(self.color.name), end = "")

    def printSoldier(self):
        if self.color == TeamColor.NONE:
            print("        ", end = "")
        else:
            print('{:^8d}'.format(self.troopCount), end = "")

    def printSpecial(self):
        if self.isResearch:
            print('{:^8s}'.format("RESEARCH"), end = "")
        elif self.isVictoryPoint:
            print('{:^8s}'.format("VICTORY"), end = "")
        elif self.isBase:
            print('{:^8s}'.format("BASE"), end = "")
        else:
            print("        ", end = "")

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