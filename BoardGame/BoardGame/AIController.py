"""
Project Name: 
File Name: AIController.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

from random import *

import InfoObjects
import board
from enums import *

class AIController(object):
    def __init__(self, color):
        self.personality = PersonalityTypes(randint(0, 4))
        self.board = None
        self.color = color
        if self.color == TeamColor.RED:
            self.myBaseLoc = [[0, 3], [0, 4], [0, 5], [0, 6]]
        elif self.color == TeamColor.YELLOW:
            self.myBaseLoc = [[3, 9], [4, 9], [5, 9], [6, 9]]
        elif self.color == TeamColor.BLUE:
            self.myBaseLoc = [[9, 3], [9, 4], [9, 5], [9, 6]]
        elif self.color == TeamColor.GREEN:
            self.myBaseLoc = [[3, 0], [4, 0], [5, 0], [6, 0]]
        self.myArmy = 0
        self.redArmy = 0
        self.yellowArmy = 0
        self.blueArmy = 0
        self.yellowArmy = 0
        self.research = InfoObjects.PlayerResearch()
        self.allResearch = InfoObjects.AllResearch()
        self.turnChoices = InfoObjects.AITurn()

    def aiTurn(self, allResearch, board):
        self.board = board
        self.allResearch = allResearch
        self.resetTurn()
        self.countArmies()
        self.turnStageOne()
        return self.turnChoices

    def resetTurn(self):
        self.myArmy = 0
        self.redArmy = 0
        self.yellowArmy = 0
        self.blueArmy = 0
        self.greenArmy = 0
        if self.color == TeamColor.RED:
            self.research = self.allResearch.redResearch
        elif self.color == TeamColor.YELLOW:
            self.research = self.allResearch.yellowResearch
        elif self.color == TeamColor.BLUE:
            self.research = self.allResearch.blueResearch
        elif self.color == TeamColor.GREEN:
            self.research = self.allResearch.greenResearch
        self.turnChoices.reset()

    def countArmies(self):
        for i in range(10):
            for j in range(10):
                if self.board.boardGrid[i][j].color == self.color:
                    self.myArmy += self.board.boardGrid[i][j].troopCount
                if self.board.boardGrid[i][j].color == TeamColor.RED:
                    self.redArmy += self.board.boardGrid[i][j].troopCount
                elif self.board.boardGrid[i][j].color == TeamColor.YELLOW:
                    self.yellowArmy += self.board.boardGrid[i][j].troopCount
                elif self.board.boardGrid[i][j].color == TeamColor.BLUE:
                    self.blueArmy += self.board.boardGrid[i][j].troopCount
                elif self.board.boardGrid[i][j].color == TeamColor.GREEN:
                    self.greenArmy += self.board.boardGrid[i][j].troopCount

    def turnStageOne(self):
        cardWeight = 0
        researchWeight = 0
        reinforceWeight = 0
        attackWeight = 0
        deployWeight = 0
        recruitWeight = 0

        # Assess personality Goals
        if self.personality == PersonalityTypes.Researcher:
            cardWeight += randint(50,75)
            reinforceWeight += randint(25,50)
            if cardWeight + reinforceWeight != 100:
                cardWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 1
            deployWeight = 2
            recruitWeight = 3

        elif self.personality == PersonalityTypes.Turtle:
            cardWeight += randint(25,50)
            reinforceWeight += randint(25,50)
            if cardWeight + reinforceWeight != 100:
                if randint(1,10) > 5:
                    cardWeight += (100 - (cardWeight + reinforceWeight))
                else:
                    reinforceWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 2
            deployWeight = 1
            recruitWeight = 3

        elif self.personality == PersonalityTypes.CenterDom:
            cardWeight += randint(10,30)
            reinforceWeight += randint(70,90)
            if cardWeight + reinforceWeight != 100:
                if randint(1,10) > 7:
                    cardWeight += (100 - (cardWeight + reinforceWeight))
                else:
                    reinforceWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 1
            deployWeight = 3
            recruitWeight = 2

        elif self.personality == PersonalityTypes.BaseRusher:
            cardWeight += randint(0,10)
            reinforceWeight += randint(90,100)
            if cardWeight + reinforceWeight != 100:
                if randint(1,10) > 9:
                    cardWeight += (100 - (cardWeight + reinforceWeight))
                else:
                    reinforceWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 2
            deployWeight = 1
            recruitWeight = 3

        elif self.personality == PersonalityTypes.DefenseWebber:
            cardWeight += randint(0,30)
            reinforceWeight += randint(70,100)
            if cardWeight + reinforceWeight != 100:
                if randint(1,10) > 6:
                    cardWeight += (100 - (cardWeight + reinforceWeight))
                else:
                    reinforceWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 3
            deployWeight = 1
            recruitWeight = 2

        # Assess points required for next research
        if (self.research.attackCost - self.research.researchPoints <= 0 or
           self.research.recruitmentCost - self.research.researchPoints <= 0 or
           self.research.deploymentCost - self.research.researchPoints <= 0):
            researchWeight += randint(150,200)

        elif (self.research.attackCost - self.research.researchPoints <= 1 or
           self.research.recruitmentCost - self.research.researchPoints <= 1 or
           self.research.deploymentCost - self.research.researchPoints <= 1):
            cardWeight += randint(25, 75)

        if ((self.myArmy - self.redArmy) / self.myArmy >= .50 or
           (self.myArmy - self.yellowArmy) / self.myArmy >= .50 or
           (self.myArmy - self.blueArmy) / self.myArmy >= .50 or
           (self.myArmy - self.greenArmy) / self.myArmy >= .50):
            reinforceWeight += randint(25,50)

        elif ((self.myArmy - self.redArmy) / self.myArmy >= .25 or
            (self.myArmy - self.yellowArmy) / self.myArmy >= .25 or
            (self.myArmy - self.blueArmy) / self.myArmy >= .25 or
            (self.myArmy - self.greenArmy) / self.myArmy >= .25):
            reinforceWeight += randint(0,25)

        for i in range(0,3):
            currentTile = self.myBaseLoc[i]
            baseTileTroops = self.board.boardGrid[currentTile[0]][currentTile[1]].troopCount
            for x in range(-2,2):
                for y in range(-2,2):
                    if (currentTile[0] + x >= 0 and currentTile[0] + x <= 8 and
                       currentTile[1] + y >= 0 and currentTile[1] + y <= 8):
                        if self.board.boardGrid[currentTile[0] + x][currentTile[1] + y].color != self.color:
                            if baseTileTroops < self.board.boardGrid[currentTile[0] + x][currentTile[1] + y].troopCount:
                                reinforceWeight += randint(25,50)
                                if x <= 1 and x >= -1 and y == 0:
                                    self.turnChoices.reinforcePos = (currentTile[0],currentTile[1])
                                elif y <= 1 and y >= -1 and x == 0:
                                    self.turnChoices.reinforcePos = (currentTile[0],currentTile[1])

        done = False
        while not done:
            if cardWeight > reinforceWeight and cardWeight > researchWeight:
                self.turnChoices.stageOne = 1
                done = True

            elif reinforceWeight >= cardWeight and reinforceWeight > researchWeight:
                if not self.assignReinforcePos():
                     reinforceWeight = 0
                else:
                    self.turnChoices.stageOne = 3
                    done = True

            elif researchWeight >= cardWeight and researchWeight >= reinforceWeight:
                if not self.chooseResearch(attackWeight, deployWeight, recruitWeight):
                    researchWeight = 0
                else:
                    self.turnChoices.stageOne = 2
                    done = True

    def assignReinforcePos(self):
        needsSetting = True
        success = False
        if self.turnChoices.reinforcePos != (-1, -1):
            if self.board.boardGrid[self.turnChoices.reinforcePos[0]][self.turnChoices.reinforcePos[1]].troopCount + self.research.deploymentResearch * 5 <= 25:
                needsSetting = False
        if needsSetting:
            hold = 0
            count = 25
            for i in range(0,3):
                if self.board.boardGrid[self.myBaseLoc[i][0]][self.myBaseLoc[i][1]].troopCount <= count:
                    hold = i
            if self.board.boardGrid[self.myBaseLoc[hold][0]][self.myBaseLoc[hold][1]].troopCount + self.research.deploymentResearch * 5 <= 25:
                self.turnChoices.reinforcePos = (self.myBaseLoc[hold][0], self.myBaseLoc[hold][1])
                success = True
        return success

    def chooseResearch(self, attackWeight, deployWeight, recruitWeight):
        chosen = False
        success = False
        if attackWeight == 3:
            if self.research.attackCost - self.research.researchPoints <= 0:
                self.turnChoices.researchChoice = 2
                success = True
            elif randint(1, 100) <= 25:
                pass
            else:
                if self.research.deploymentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = 1
                    success = True
                elif self.research.recruitmentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = 3
                    success = True
                
        elif deployWeight == 3:
            if self.research.deploymentCost - self.research.researchPoints <= 0:
                self.turnChoices.researchChoice = 1
            elif randint(1, 100) <= 25:
                pass
            else:
                if self.research.attackCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = 2
                    success = True
                elif self.research.recruitmentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = 3
                    success = True

        elif recruitWeight == 3:
            if self.research.recruitmentCost - self.research.researchPoints <= 0:
                self.turnChoices.researchChoice = 3
            elif randint(1, 100) <= 25:
                pass
            else:
                if self.research.deploymentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = 1
                    success = True
                elif self.research.attackCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = 2
                    success = True
        return success


    def turnStageTwo(self):
        pass