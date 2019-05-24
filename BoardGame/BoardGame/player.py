"""
Project Name: 
File Name: player.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

from random import *

class PlayerInfo(object):
    def __init__(self, color, isNPC):
        self.isNPC = isNPC
        self.isAlive = True
        self.color = color
        self.commandPoints = 0
        self.deploymentResearch = 1
        self.deploymentCost = 4
        self.attackResearch = 1
        self.attackCost = 8
        self.recruitmentResearch = 1
        self.recruitmentCost = 8
        self.researchPoints = 0

    def displayResearch(self, includePoints, includeCosts):
        print("{:17s}{:6s}".format("Player: ", self.color.name))
        if includePoints:
            print("{:17s}{:<2d}".format("Current Points: ", self.researchPoints))
        if not includeCosts:
            print("{:17s}{:1d}".format("Deployment: ", self.deploymentResearch))
            print("{:17s}{:1d}".format("Attack: ", self.attackResearch))
            print("{:17s}{:1d}".format("Recruitment: ", self.recruitmentResearch), end = "\n\n")
        elif includeCosts:
            print("{:17s}{:1d} - Upgrade Cost {:2d}".format("1 - Deployment: ", self.deploymentResearch, self.deploymentCost))
            print("{:17s}{:1d} - Upgrade Cost {:2d}".format("2 - Attack: ", self.attackResearch, self.attackCost))
            print("{:17s}{:1d} - Upgrade Cost {:2d}".format("3 - Recruitment: ", self.recruitmentResearch, self.recruitmentCost), end = "\n\n")

    def displayName(self):
        print(self.color.name)

    def getIsNPC(self):
        return self.isNPC

    def getTeamColor(self):
        return self.color

    def getReinforcements(self):
        return 5 * self.recruitmentResearch

    def getDeployment(self):
        return self.deploymentResearch

    def getIsAlive(self):
        return self.isAlive

    def getHasWon(self):
        return self.commandPoints >= 5

    def gainCommandPoints(self, points):
        self.commandPoints += points

    def takeResearchCard(self):
        psuedoRandom = randint(1, 100)
        if psuedoRandom >= 1 and psuedoRandom <= 40:
            self.researchPoints += 1
            print("You recieve 1 research point for a total of {}".format(self.researchPoints))
        elif psuedoRandom > 40 and psuedoRandom <= 75:
            self.researchPoints += 2
            print("You recieve 2 research points for a total of {}".format(self.researchPoints))
        elif psuedoRandom > 75 and psuedoRandom <= 90:
            self.researchPoints += 3
            print("You recieve 3 research points for a total of {}".format(self.researchPoints))
        else:
            self.researchPoints += 4
            print("You recieve 4 research points for a total of {}".format(self.researchPoints))

    def performResearch(self, choice):
        success = False
        if choice == "1":
            if self.deploymentResearch == 3:
                print("Deployment Research is already at max level.")
            if self.researchPoints >= self.deploymentCost:
                self.deploymentResearch += 1
                self.researchPoints -= self.deploymentCost
                self.deploymentCost *= 2
                print("Deployment research increased to level {}".format(self.deploymentResearch))
                success = True
        elif choice == "2":
            if self.attackResearch == 3:
                print("Attack Research is already at max level.")
            if self.researchPoints >= self.attackCost:
                self.attackResearch += 1
                self.researchPoints -= self.attackCost
                self.attackCost *= 2
                print("Attack research increased to level {}".format(self.attackResearch))
                success = True
        elif choice == "3":
            if self.recruitmentResearch == 3:
                print("Recruitment Research is already at max level.")
            if self.researchPoints >= self.recruitmentCost:
                self.recruitmentResearch += 1
                self.researchPoints -= self.recruitmentCost
                self.recruitmentCost *= 2
                print("Recruitment research increased to level {}".format(self.recruitmentResearch))
                success = True
        else:
            print("Invalid Choice!")
        return success

    def kill(self):
        self.isAlive = False