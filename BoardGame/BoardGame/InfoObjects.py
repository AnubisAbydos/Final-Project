"""
Project Name: 
File Name: AITurn.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

class AITurn(object):
    def __init__(self):
        self.stageOne = 0
        self.researchChoice = 0
        self.reinforcePos = (-1,-1)

    def reset(self):
        self.stageOne = 0
        self.researchChoice = 0
        self.reinforcePos = (-1,-1)

class PlayerResearch(object):
    def __init__(self):
        self.deploymentResearch = 1
        self.deploymentCost = 4
        self.attackResearch = 1
        self.attackCost = 8
        self.recruitmentResearch = 1
        self.recruitmentCost = 8
        self.researchPoints = 0

class AllResearch(object):
    def __init__(self):
        self.redResearch = PlayerResearch()
        self.blueResearch = PlayerResearch()
        self.yellowResearch = PlayerResearch()
        self.greenResearch = PlayerResearch()
