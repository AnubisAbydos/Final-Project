"""
Project Name: BoardGame
File Name: player.py
Author: Lex Hall
Last Updated: 7/29/19
Python Version: 3.6
"""

from random import *

import AIController
import infoObjects

class PlayerInfo(object):
    def __init__(self, color):
        self.isNPC = False
        self.isAlive = True
        self.color = color
        self.victoryPoints = 0
        self.research = infoObjects.PlayerResearch()
        self.aiController = None

    def getReinforcements(self):
        return 5 * self.research.recruitmentResearch

    def getHasWon(self):
        return self.victoryPoints >= 5

    ### Assigns isNPC true and builds a controller
    def assignAI(self):
        self.isNPC = True
        self.aiController = AIController.AIController(self.color)

    def takeResearchCard(self):
        psuedoRandom = randint(1, 100)
        if psuedoRandom >= 1 and psuedoRandom <= 40:
            self.research.researchPoints += 1
            print("You recieve 1 research point for a total of {}".format(self.research.researchPoints))
        elif psuedoRandom > 40 and psuedoRandom <= 75:
            self.research.researchPoints += 2
            print("You recieve 2 research points for a total of {}".format(self.research.researchPoints))
        elif psuedoRandom > 75 and psuedoRandom <= 90:
            self.research.researchPoints += 3
            print("You recieve 3 research points for a total of {}".format(self.research.researchPoints))
        else:
            self.research.researchPoints += 4
            print("You recieve 4 research points for a total of {}".format(self.research.researchPoints))

    def performResearch(self, choice):
        success = False
        if choice == "1":
            if self.research.deploymentResearch == 3:
                print("Deployment Research is already at max level.")
            if self.research.researchPoints >= self.research.deploymentCost:
                self.research.deploymentResearch += 1
                self.research.researchPoints -= self.research.deploymentCost
                self.research.deploymentCost *= 2
                print("Deployment research increased to level {}".format(self.research.deploymentResearch))
                success = True
        elif choice == "2":
            if self.research.attackResearch == 3:
                print("Attack Research is already at max level.")
            if self.research.researchPoints >= self.research.attackCost:
                self.research.attackResearch += 1
                self.research.researchPoints -= self.research.attackCost
                self.research.attackCost *= 2
                print("Attack research increased to level {}".format(self.research.attackResearch))
                success = True
        elif choice == "3":
            if self.research.recruitmentResearch == 3:
                print("Recruitment Research is already at max level.")
            if self.research.researchPoints >= self.research.recruitmentCost:
                self.research.recruitmentResearch += 1
                self.research.researchPoints -= self.research.recruitmentCost
                self.research.recruitmentCost *= 2
                print("Recruitment research increased to level {}".format(self.research.recruitmentResearch))
                success = True
        else:
            print("Invalid Choice!")
        return success

    def displayResearch(self, includePoints, includeCosts):
        print("{:17s}{:6s}".format("Player: ", self.color.name))
        if includePoints:
            print("{:17s}{:<2d}".format("Current Points: ", self.research.researchPoints))
        if not includeCosts:
            print("{:17s}{:1d}".format("Deployment: ", self.research.deploymentResearch))
            print("{:17s}{:1d}".format("Attack: ", self.research.attackResearch))
            print("{:17s}{:1d}".format("Recruitment: ", self.research.recruitmentResearch), end = "\n\n")
        elif includeCosts:
            print("{:17s}{:1d} - Upgrade Cost {:2d}".format("1 - Deployment: ", self.research.deploymentResearch, self.research.deploymentCost))
            print("{:17s}{:1d} - Upgrade Cost {:2d}".format("2 - Attack: ", self.research.attackResearch, self.research.attackCost))
            print("{:17s}{:1d} - Upgrade Cost {:2d}".format("3 - Recruitment: ", self.research.recruitmentResearch, self.research.recruitmentCost), end = "\n\n")

    def displayName(self):
        print(self.color.name)