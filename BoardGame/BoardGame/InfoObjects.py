"""
Project Name: BoardGame
File Name: infoObjects.py
Author: Lex Hall
Last Updated: 7/29/2019
Python Version: 3.6
"""


''' CLASS AITurn
Stores the information needed to perform an AI turn
Filled by an AIController and used in game to perform a turn
'''
class AITurn(object):
    def __init__(self):
        self.stageOne = 0
        self.researchChoice = 0
        self.reinforcePos = (-1,-1)
        self.numberOfMoves = 0
        self.moves = []

    def reset(self):
        self.stageOne = 0
        self.researchChoice = 0
        self.reinforcePos = (-1,-1)
        self.numberOfMoves = 0
        self.moves = []


''' CLASS MoveOrder
Used to store a MoveOrder in the moves of AITurn
'''
class MoveOrder(object):
    def __init__(self):
        self.fromLocation = (-1, -1)
        self.toLocation = (-1, -1)
        self.troopsToMove = -1
        self.goalStatement = None


''' CLASS PlayerResearch
Stores a single players research levels, costs and points
Costs refer to the number of points required for upgrade
'''
class PlayerResearch(object):
    def __init__(self):
        self.deploymentResearch = 1
        self.deploymentCost = 4
        self.attackResearch = 1
        self.attackCost = 8
        self.recruitmentResearch = 1
        self.recruitmentCost = 8
        self.researchPoints = 0


''' CLASS AllResearch
Stores all players PlayerResearch Objects
'''
class AllResearch(object):
    def __init__(self):
        self.redResearch = PlayerResearch()
        self.blueResearch = PlayerResearch()
        self.yellowResearch = PlayerResearch()
        self.greenResearch = PlayerResearch()

''' CLASS ArmyPath
Stores army information to be used with the A* pathfinding
Path stores the results of the pathfinding algorithm
'''
class ArmyPath(object):
    def __init__(self, x, y, count, isCenter):
        self.startLoc = (x, y)
        self.goalStatement = None
        self.goal = (-1, -1)
        self.startIsCenter = isCenter
        self.troopCount = count
        self.path = []
        self.finalFScore = -1
        self.firstMoveFScore = -1

''' CLASS PathTile
stores information for each tile in the A* algorithm
'''
class PathTile(object):
    def __init__(self, x, y, isEnemy, isCenter):
        self.location = (x, y)
        self.isEnemy = isEnemy
        self.isCenter = isCenter
        self.troopCount = 0
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
    
    # Overrides the < operator for pathTiles, for use by the priorityQueue
    def __lt__(self, value):
        return self.f < value.f

