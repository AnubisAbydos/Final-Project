"""
Project Name: BoardGame
File Name: AIController.py
Author: Lex Hall
Last Updated: 7/30/19
Python Version: 3.6
"""

from random import *
import heapq
import math

import infoObjects
import board
from enums import *

''' CLASS PriorityQueue
Holds the information to run a sorted queue given item with priority
Used exclusively by the A* Pathfinding Algortihm below
'''
class PriorityQueue(object):
    def __init__(self):
        self.items = []

    # Place item into items queue sorted by priority number (lower numbers at front of queue)
    def push(self, item, priority):
        heapq.heappush(self.items, (priority, item))

    # returns lowest priority number
    def pop(self):
        return heapq.heappop(self.items)[1]

    def isEmpty(self):
        return len(self.items) == 0
    
    # determines if a given item already exists within the queue
    def exists(self, findItem):
        exists = False
        for item in self.items:
            if item[1].location == findItem.location:
                exists = True
        return exists


''' CLASS AIController
Holds all relevant information and decision making processes for the AI possessing a player
'''
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
        self.research = infoObjects.PlayerResearch()
        self.allResearch = infoObjects.AllResearch()
        self.turnChoices = infoObjects.AITurn()

    # Called by game to build AI turnChoices
    def aiTurnStageOne(self, allResearch, board):
        # update and prepare for choices
        self.board = board
        self.allResearch = allResearch
        self.resetTurn()
        self.countArmies()

        # create choices for stage one
        self.turnStageOne()

    def aiTurnStageTwo(self):
        self.turnStageTwo()

    # Resets turn information and brings it up to date
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

    # Iterate over board and count troop counts for each player
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
            reinforceWeight += randint(0,25)
            if cardWeight + reinforceWeight != 100:
                reinforceWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 1
            deployWeight = 2
            recruitWeight = 3
            if self.research.attackResearch + self.research.deploymentResearch + self.research.recruitmentResearch >= 6:
                if randint(1, 10) > 5:
                    self.personality = PersonalityTypes.BaseRusher
                else:
                    self.personality = PersonalityTypes.CenterDom

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
            # TODO Add personality shift after set army or research amount

        elif self.personality == PersonalityTypes.CenterDom:
            cardWeight += randint(10,30)
            reinforceWeight += randint(50,70)
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
            reinforceWeight += randint(80,90)
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
            reinforceWeight += randint(40,70)
            if cardWeight + reinforceWeight != 100:
                if randint(1,10) > 6:
                    cardWeight += (100 - (cardWeight + reinforceWeight))
                else:
                    reinforceWeight += (100 - (cardWeight + reinforceWeight))
            attackWeight = 3
            deployWeight = 1
            recruitWeight = 2
            # TODO Personality shift

        # Assess points required for next research
        if (self.research.attackCost - self.research.researchPoints <= 0 or
           self.research.recruitmentCost - self.research.researchPoints <= 0 or
           self.research.deploymentCost - self.research.researchPoints <= 0):
            researchWeight += randint(150,200)

        elif (self.research.attackCost - self.research.researchPoints <= 1 or
           self.research.recruitmentCost - self.research.researchPoints <= 1 or
           self.research.deploymentCost - self.research.researchPoints <= 1):
            cardWeight += randint(25, 75)

        if self.myArmy == 0:
            reinforceWeight += randint(150, 200)

        elif ((self.myArmy - self.redArmy) / self.myArmy >= .50 or
           (self.myArmy - self.yellowArmy) / self.myArmy >= .50 or
           (self.myArmy - self.blueArmy) / self.myArmy >= .50 or
           (self.myArmy - self.greenArmy) / self.myArmy >= .50):
            reinforceWeight += randint(25,50)

        elif ((self.myArmy - self.redArmy) / self.myArmy >= .25 or
            (self.myArmy - self.yellowArmy) / self.myArmy >= .25 or
            (self.myArmy - self.blueArmy) / self.myArmy >= .25 or
            (self.myArmy - self.greenArmy) / self.myArmy >= .25):
            reinforceWeight += randint(0,25)

        for i in range(4):
            currentTile = self.myBaseLoc[i]
            baseTileTroops = self.board.boardGrid[currentTile[0]][currentTile[1]].troopCount
            for x in range(-2,3):
                for y in range(-2,3):
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
                    if reinforceWeight == 0 and cardWeight == 0:
                        self.turnChoices.stageOne = 1
                        done = True
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
            for i in range(4):
                if self.board.boardGrid[self.myBaseLoc[i][0]][self.myBaseLoc[i][1]].troopCount <= count:
                    hold = i
                    count = self.board.boardGrid[self.myBaseLoc[i][0]][self.myBaseLoc[i][1]].troopCount
            if self.board.boardGrid[self.myBaseLoc[hold][0]][self.myBaseLoc[hold][1]].troopCount + self.research.deploymentResearch * 5 <= 25:
                self.turnChoices.reinforcePos = (self.myBaseLoc[hold][0], self.myBaseLoc[hold][1])
                success = True
        return success

    def chooseResearch(self, attackWeight, deployWeight, recruitWeight):
        chosen = False
        success = False
        if attackWeight == 3:
            if self.research.attackCost - self.research.researchPoints <= 0:
                self.turnChoices.researchChoice = "2"
                success = True
            elif randint(1, 100) <= 25:
                pass
            else:
                if self.research.deploymentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = "1"
                    success = True
                elif self.research.recruitmentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = "3"
                    success = True
                
        elif deployWeight == 3:
            if self.research.deploymentCost - self.research.researchPoints <= 0:
                self.turnChoices.researchChoice = "1"
                success = True
            elif randint(1, 100) <= 25:
                pass
            else:
                if self.research.attackCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = "2"
                    success = True
                elif self.research.recruitmentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = "3"
                    success = True

        elif recruitWeight == 3:
            if self.research.recruitmentCost - self.research.researchPoints <= 0:
                self.turnChoices.researchChoice = "3"
                success = True
            elif randint(1, 100) <= 25:
                pass
            else:
                if self.research.deploymentCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = "1"
                    success = True
                elif self.research.attackCost - self.research.researchPoints <= 0:
                    self.turnChoices.researchChoice = "2"
                    success = True
        return success


    def turnStageTwo(self):
        # TODO set armies to remember goals for set time
        armies = self.buildArmyPathsArray()

        for army in armies:
            if self.personality == PersonalityTypes.Researcher:
                if randint(1, 100) <= 75:
                    army.goalStatement = GoalStatement.CenterResearch
                else:
                    army.goalStatement = GoalStatement.CenterVictory

            elif self.personality == PersonalityTypes.Turtle:
                if army.troopCount == 25:
                    army.goalStatement = GoalStatement.CenterVictory
                elif randint(1, 100) <= 50:
                    if army.troopCount < 25:
                        army.goalStatement = GoalStatement.DoomStack
                    else:
                        army.goalStatement = GoalStatement.DefenseLocation
                else:
                    army.goalStatement = GoalStatement.DefenseLocation

            elif self.personality == PersonalityTypes.CenterDom:
                if randint(1, 100) <= 75:
                    army.goalStatement = GoalStatement.CenterVictory
                else:
                    army.goalStatement = GoalStatement.CenterResearch

            elif self.personality == PersonalityTypes.BaseRusher:
                if army.troopCount == 25:
                    army.goalStatement = GoalStatement.BaseAttack
                elif randint(1, 100) <= 75:
                    army.goalStatement = GoalStatement.BaseAttack
                else:
                    if army.troopCount < 25:
                        army.goalStatement = GoalStatement.DoomStack
                    else:
                        army.goalStatement = GoalStatement.BaseAttack

            elif self.personality == PersonalityTypes.DefenseWebber:
                if army.troopCount == 25:
                    army.goalStatement = GoalStatement.CenterVictory
                if randint(1, 100) <= 75:
                    army.goalStatement = GoalStatement.DefenseLocation
                else:
                    if army.troopCount < 25:
                        army.goalStatement = GoalStatement.DoomStack
                    else:
                        army.goalStatement = GoalStatement.DefenseLocation

            if army.startIsCenter and army.troopCount > 5:
                army.goalStatement = GoalStatement.NONE

            # Build army goal after assigning statement
            if army.goalStatement != GoalStatement.NONE:
                self.buildGoal(army, 1, (army.startLoc[0], army.startLoc[1]))
            # If army has a goal build its path
            if army.goalStatement != GoalStatement.NONE:
                self.buildPath(army)
        
        # If there are armies left take the first one as the lowest for sorting by F Score
        if len(armies) > 0:
            currentLowestArmy = armies[0]
        numberOfMoves = self.research.deploymentResearch
        armiesToMove = []
        if len(armies) < numberOfMoves:
            numberOfMoves = len(armies)
        self.turnChoices.numberOfMoves = numberOfMoves
        for i in range(numberOfMoves):
            for army in armies:
                if army.finalFScore < currentLowestArmy.finalFScore and army.finalFScore != -1:
                    currentLowestArmy = army
                elif army.finalFScore == currentLowestArmy.finalFScore and army.finalFScore != -1:
                    if army.firstMoveFScore < currentLowestArmy.firstMoveFScore and army.firstMoveFScore != -1:
                        currentLowestArmy = army
            if numberOfMoves > 1:
                armies.remove(currentLowestArmy)
            if currentLowestArmy.goalStatement != GoalStatement.NONE:
                armiesToMove.append(currentLowestArmy)
            if len(armies) > 0:
                currentLowestArmy = armies[0]
        for army in armiesToMove:
            self.createMoveOrder(army)
        del armies

    def buildArmyPathsArray(self):
        returnArray = []
        isCenter = False
        for i in range(10):
            for j in range(10):
                if self.board.boardGrid[i][j].color == self.color and self.board.boardGrid[i][j].troopCount > 0:
                    if self.board.boardGrid[i][j].isResearch or self.board.boardGrid[i][j].isVictoryPoint:
                        isCenter = True
                    else:
                        isCenter = False
                    returnArray.append(infoObjects.ArmyPath(i, j, self.board.boardGrid[i][j].troopCount, isCenter))
        return returnArray

    def buildPath(self, army):
        openList = PriorityQueue()
        start = infoObjects.PathTile(army.startLoc[0], army.startLoc[1], False, army.startIsCenter)
        goal = army.goal
        openList.push(start, 0)
        closedList = set()
        done = False

        while not done:
            if not openList.isEmpty():
                lowestFTile = openList.pop()

            closedList.add(lowestFTile)

            neighbors = self.getNeighbors(lowestFTile)

            for neighbor in neighbors:
                if neighbor.location == goal:
                    done = True
                    self.updateTile(neighbor, lowestFTile, start, goal)
                    self.updateArmyPath(army, neighbor)
                    del openList
                    del closedList
                    break
                elif not openList.exists(neighbor) and not self.checkInClosedList(closedList, neighbor):
                    self.updateTile(neighbor, lowestFTile, start, goal)
                    openList.push(neighbor, neighbor.f)

    def checkInClosedList(self, closedList, item):
        found = False
        for each in closedList:
            if each.location == item.location:
                found = True
        return found

    def updateArmyPath(self, army, finalTile):
        finalFScore = 0
        tile = finalTile
        lastFScore = 0
        while tile.location != army.startLoc:
            lastFScore = tile.f
            finalFScore += lastFScore
            army.path.append(tile)
            tile = tile.parent
        army.firstMoveFScore = lastFScore
        army.finalFScore = finalFScore

    ### RECURSIVE FUNCTION - Uses spiral search loops to find goal location for given army
    def buildGoal(self, army, searchLoop, currentLocation):
        x = currentLocation[0]
        y = currentLocation[1]
        # First Tile : UP ONE
        if searchLoop == 1:
            y = y - 1
            if (-1 < x <= 9) and (-1 < y <= 9):
                    tile = self.board.boardGrid[x][y]
                    if self.checkTileForGoal(tile, army):
                        army.goal = (x, y)
                        return
        
        # Could not find goal
        if searchLoop >= 11:
            army.goalStatement = GoalStatement.NONE
            return

        # RIGHT Loop
        for i in range((searchLoop * 2) - 1):
            x = x + 1
            if (-1 < x <= 9) and (-1 < y <= 9):
                tile = self.board.boardGrid[x][y]
                if self.checkTileForGoal(tile, army):
                    army.goal = (x, y)
                    return
        
        # DOWN Loop
        for i in range(searchLoop * 2):
            y = y + 1
            if (-1 < x <= 9) and (-1 < y <= 9):
                tile = self.board.boardGrid[x][y]
                if self.checkTileForGoal(tile, army):
                    army.goal = (x, y)
                    return

        # LEFT
        for i in range(searchLoop * 2):
            x = x - 1
            if (-1 < x <= 9) and (-1 < y <= 9):
                tile = self.board.boardGrid[x][y]
                if self.checkTileForGoal(tile, army):
                    army.goal = (x, y)
                    return

        # UP
        for i in range((searchLoop * 2) + 1):
            y = y - 1
            if (-1 < x <= 9) and (-1 < y <= 9):
                tile = self.board.boardGrid[x][y]
                if self.checkTileForGoal(tile, army):
                    army.goal = (x, y)
                    return
        self.buildGoal(army, searchLoop + 1, (x, y))

    def checkTileForGoal(self, tile, army):
        if army.goalStatement == GoalStatement.BaseAttack:
            if tile.isBase and (tile.color != self.color):
                return True
        if army.goalStatement == GoalStatement.CenterResearch:
            if tile.isResearch:
                return True
        if army.goalStatement == GoalStatement.CenterVictory:
            if tile.isVictoryPoint:
                return True
        if army.goalStatement == GoalStatement.DefenseLocation:
            # TODO determine what a defenseLocation is (EQUAL TO BaseAttack FOR NOW!)
            if tile.isBase and (tile.color != self.color):
                return True
        if army.goalStatement == GoalStatement.DoomStack:
            if tile.color == self.color and tile.troopCount < 25:
                return True
        return False

    def checkForEnemies(self, start):
        isEnemyNearby = False
        if (0 < start.location[0] - 1 <= 9) and (0 < start.location[1] <= 9):
            if self.board.boardGrid[start.location[0] - 1][start.location[1]].color != TeamColor.NONE:
                if self.board.boardGrid[start.location[0] - 1][start.location[1]].color != self.color:
                    isEnemyNearby = True
        if (0 < start.location[0] + 1 <= 9) and (0 < start.location[1] <= 9):
            if self.board.boardGrid[start.location[0] + 1][start.location[1]].color != TeamColor.NONE:
                if self.board.boardGrid[start.location[0] + 1][start.location[1]].color != self.color:
                    isEnemyNearby = True
        if (0 < start.location[0] <= 9) and (0 < start.location[1] - 1 <= 9):
            if self.board.boardGrid[start.location[0]][start.location[1] - 1].color != TeamColor.NONE:
                if self.board.boardGrid[start.location[0]][start.location[1] - 1].color != self.color:
                    isEnemyNearby = True
        if (0 < start.location[0] <= 9) and (0 < start.location[1] + 1 <= 9):
            if self.board.boardGrid[start.location[0]][start.location[1] + 1].color != TeamColor.NONE:
                if self.board.boardGrid[start.location[0]][start.location[1] + 1].color != self.color:
                    isEnemyNearby = True
        return isEnemyNearby

    def createMoveOrder(self, army):
        moveOrder = infoObjects.MoveOrder()
        moveOrder.goalStatement = army.goalStatement
        moveOrder.fromLocation = army.startLoc

        destination = army.path.pop()
        moveOrder.toLocation = destination.location

        if destination.isEnemy:
            moveOrder.troopsToMove = int(math.ceil(destination.troopCount / self.research.attackResearch))
        elif army.troopCount + destination.troopCount >= 25:
            moveOrder.troopsToMove = 25 - destination.troopCount
        else:
            moveOrder.troopsToMove = army.troopCount
        self.turnChoices.moves.append(moveOrder)

    def getNeighbors(self, parentTile):
        tiles = []
        if parentTile.location[0] + 1 <= 9:
            newLocation = (parentTile.location[0] + 1, parentTile.location[1])
            tiles.append(self.createTileFromBoard(newLocation))
        if parentTile.location[0] - 1 >= 0:
            newLocation = (parentTile.location[0] - 1, parentTile.location[1])
            tiles.append(self.createTileFromBoard(newLocation))
        if parentTile.location[1] + 1 <= 9:
            newLocation = (parentTile.location[0], parentTile.location[1] + 1)
            tiles.append(self.createTileFromBoard(newLocation))
        if parentTile.location[1] - 1 >= 0:
            newLocation = (parentTile.location[0], parentTile.location[1] - 1)
            tiles.append(self.createTileFromBoard(newLocation))
        return tiles

    def createTileFromBoard(self, boardLocation):
        boardTile = self.board.boardGrid[boardLocation[0]][boardLocation[1]]
        if boardTile.isResearch or boardTile.isVictoryPoint:
            isCenter = True
        else:
            isCenter = False
        tile = infoObjects.PathTile(boardLocation[0], boardLocation[1], False, isCenter)
        if boardTile.color.value != 0:
            tile.isEnemy = (boardTile.color != self.color)
            tile.troopCount = boardTile.troopCount
        return tile

    def updateTile(self, neighbor, parentTile, start, goal):
        neighbor.g = self.calculateG(neighbor, start)
        neighbor.h = self.calculateH(neighbor, goal)
        neighbor.parent = parentTile
        neighbor.f = neighbor.g + neighbor.h

    def calculateG(self, neighbor, start):
        g = 0
        moves = abs(neighbor.location[0] - start.location[0]) + abs(neighbor.location[1] - start.location[1])
        if moves == 1:
            troopScore = 50 - start.troopCount * 2
            g += troopScore
            if neighbor.isEnemy:
                if neighbor.troopCount <= start.troopCount:
                    g += -100
                    return g

                else:
                    # TODO add chance for an emergency retreat function or an attack (check for if center as well)
                    pass

            # If the first move is not an enemy continue calculate normally
            else:
                pass

        if self.checkForEnemies(neighbor):
            g += 100
        elif not neighbor.isEnemy and neighbor.troopCount > 0 and neighbor.troopCount < 25:
            g += 10
        elif neighbor.isCenter:
            if start.troopCount >= 5:
                g += 0
            else:
                g += 100
        else:
            g += 20
        return g

    def calculateH(self, neighbor, goal):
        return (abs(neighbor.location[0] - goal[0]) + abs(neighbor.location[1] - goal[1])) * 10
