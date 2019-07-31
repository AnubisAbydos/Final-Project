"""
Project Name: BoardGame
File Name: game.py
Author: Lex Hall
Last Updated: 7/29/19
Python Version: 3.6
"""

from os import system, name
import time
import csv

import tile
import board
import player
import infoObjects
from enums import *

''' CLASS Game
Contains all information to run a full game of Kings of Men
Holds board and player information as well as runs the gameLoop
'''
class Game(object):
    def __init__(self):
        self.board = board.Board()
        self.redPlayer = player.PlayerInfo(TeamColor.RED)
        self.bluePlayer = player.PlayerInfo(TeamColor.BLUE)
        self.yellowPlayer = player.PlayerInfo(TeamColor.YELLOW)
        self.greenPlayer = player.PlayerInfo(TeamColor.GREEN)
        self.allResearch = infoObjects.AllResearch()
        self.debug = True
        if self.debug:
            self.turnNumber = 1
            with open('turn_Output.csv', mode='w') as turnOutput:
                turnWriter = csv.writer(turnOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                turnWriter.writerow(['Turn', 'Player', 'Personality', 'Army Count', 'Deployment', 'Attack', 'Recruitment',
                                     'Res Points', 'TurnOne', 'ResearchChoice', 'Reinforce', '# of Moves', 'Victory Points'])

    ### Called by main to begin the game
    def play(self):
        self.assignAIPlayers()
        self.gameLoop()

    ### Assigns AI to each player either automatically or confirming for each
    def assignAIPlayers(self):
        if self.debug:
            self.redPlayer.assignAI()
            self.bluePlayer.assignAI()
            self.yellowPlayer.assignAI()
            self.greenPlayer.assignAI()
        else:
            isAI = input("Is RedPlayer AI? (0, 1): ")
            if isAI == "1":
                self.redPlayer.assignAI()
            isAI = input("Is BluePlayer AI? (0, 1): ")
            if isAI == "1":
                self.bluePlayer.assignAI()
            isAI = input("Is YellowPlayer AI? (0, 1): ")
            if isAI == "1":
                self.yellowPlayer.assignAI()
            isAI = input("Is GreenPlayer AI? (0, 1): ")
            if isAI == "1":
                self.greenPlayer.assignAI()
    
    ### Controls game loop continues until a player wins
    def gameLoop(self):
        done = False
        winningPlayer = None

        while not done:
            # Red Player
            if self.redPlayer.isAlive:
                self.board.applyAttrition(self.redPlayer)
                if self.redPlayer.isNPC:
                    self.aiTurn(self.redPlayer)
                else:
                    self.playerTurn(self.redPlayer)
                self.allResearch.redResearch = self.redPlayer.research
                if self.redPlayer.getHasWon():
                    done = True
                    winningPlayer = self.redPlayer
                    break

            # Yellow Player
            if self.yellowPlayer.isAlive:
                self.board.applyAttrition(self.yellowPlayer)
                if self.yellowPlayer.isNPC:
                    self.aiTurn(self.yellowPlayer)
                else:
                    self.playerTurn(self.yellowPlayer)
                self.allResearch.yellowResearch = self.yellowPlayer.research
                if self.yellowPlayer.getHasWon():
                    done = True
                    winningPlayer = self.yellowPlayer
                    break

            # Blue Player
            if self.bluePlayer.isAlive:
                self.board.applyAttrition(self.bluePlayer)
                if self.bluePlayer.isNPC:
                    self.aiTurn(self.bluePlayer)
                else:
                    self.playerTurn(self.bluePlayer)
                self.allResearch.blueResearch = self.bluePlayer.research
                if self.bluePlayer.getHasWon():
                    done = True
                    winningPlayer = self.bluePlayer
                    break
                
            # Green Player
            if self.greenPlayer.isAlive:
                self.board.applyAttrition(self.greenPlayer)
                if self.greenPlayer.isNPC:
                    self.aiTurn(self.greenPlayer)
                else:
                    self.playerTurn(self.greenPlayer)
                self.allResearch.greenResearch = self.greenPlayer.research
                if self.greenPlayer.getHasWon():
                    done = True
                    winningPlayer = self.greenPlayer
            if self.debug:
                self.turnNumber += 1
                
        # Victory
        self.clearScreen()
        print("Victory! Congratulations...")
        winningPlayer.displayName()

    ### Calls each players print research function
    def displayAllResearch(self):
        self.redPlayer.displayResearch(False, False)
        self.bluePlayer.displayResearch(False, False)
        self.yellowPlayer.displayResearch(False, False)
        self.greenPlayer.displayResearch(False, False)

    ### Clears screen for windows or unix systems
    def clearScreen(self):
        if name == 'nt': 
            _ = system('cls')

        else:
            _ = system('clear')

    # TODO Refactor to seperate Class humanController
    def playerTurn(self, player):
        turnDone = False
        boardToggle = True
        turnStage = 0
        while turnStage == 0:
            print("Player: ", end = "")
            player.displayName()
            print("1 - Display board")
            print("2 - Display your Research")
            print("3 - Display all Research")
            if turnStage == 0:
                print("4 - Begin Turn")
            elif turnStage == 1:
                print("4 - Continue Turn")
            choice = input("Choose an action: ")
            if choice == "1":
                self.clearScreen()
                self.board.displayBoard()
            elif choice == "2":
                self.clearScreen()
                player.displayResearch(True, False)
            elif choice == "3":
                self.clearScreen()
                self.displayAllResearch()
            elif choice == "4":
                self.clearScreen()
                if turnStage == 0:
                    done = False
                    while not done:
                        print("Upkeep Phase")
                        print("1 - Take Research Card")
                        print("2 - Perform Research")
                        print("3 - Deploy Reinforcements")
                        choice = input("Input choice: ")
                        if choice == "1":
                            self.clearScreen()
                            player.takeResearchCard()
                            print("\n")
                            done = True
                            input("Press 'Enter' to continue turn...")
                            self.clearScreen()
                        elif choice == "2":
                            self.clearScreen()
                            player.displayResearch(True, True)
                            print("4 - Cancel")
                            choice = input("Choose research to perform: ")
                            if choice != "4":
                                self.clearScreen()
                                if player.performResearch(choice):
                                    print("\n")
                                    done = True
                                    input("Press 'Enter' to continue turn...")
                                    self.clearScreen()
                            else:
                                self.clearScreen()
                        elif choice == "3":
                            self.clearScreen()
                            self.board.displayBoard()
                            print("You recieve {} troops.".format(player.getReinforcements()))
                            selectedSquare = input("Input grid location to place them. (Must be inside one of your base squares): ")
                            self.clearScreen()
                            if self.processGridInput(selectedSquare, "a1", player, True, False, False):
                                print("{} Troops successfully deployed to tile {}\n".format(player.getReinforcements(), selectedSquare.upper()))
                                done = True
                                input("Press 'Enter' to continue turn...")
                                self.clearScreen()
                            else:
                                pass
                        else:
                            print("Invalid Input", end = "\n\n")
                turnStage = 1
            else:
                print("Invalid Input", end = "\n\n")

        moves = 0
        while turnStage == 1 or turnStage == 2:
            if boardToggle:
                self.board.displayBoard()
            if turnStage == 1:
                print("Movement Phase")
            else:
                print("Continue Movement Phase")
            print("1 - Toggle Board")
            print("2 - Move Troops to new square")
            print("3 - Move Troops to attack")
            print("4 - Skip Movement Phase")
            choice = input("Input Choice: ")
            if choice == "1":
                self.clearScreen()
                boardToggle = not boardToggle
            elif choice == "2":
                self.clearScreen()
                self.board.displayBoard()
                firstSquare = input("Input first grid location: ")
                secondSquare = input("Input second grid location: ")
                if self.processGridInput(firstSquare, secondSquare, player, False, False, True):
                    self.clearScreen()
                    print("Troop Movement Successful.")
                    moves += 1
                    if moves != player.research.deploymentResearch:
                        turnStage = 2
                        input("Press 'Enter' to continue movement...")
                        self.clearScreen()
                    else:
                        input("Press 'Enter' to end turn...")
                        turnStage = -1
                        self.clearScreen()
            elif choice == "3":
                self.clearScreen()
                self.board.displayBoard()
                firstSquare = input("Input first grid location: ")
                secondSquare = input("Input second grid location: ")
                if self.processGridInput(firstSquare, secondSquare, player, False, True, False):
                    self.clearScreen()
                    print("Attack executed.")
                    moves += 1
                    if moves != player.research.deploymentResearch:
                        turnStage = 2
                        input("Press 'Enter' to continue movement...")
                        self.clearScreen()
                    else:
                        input("Press 'Enter' to end turn...")
                        turnStage = -1
                        self.clearScreen()
            elif choice == "4":
                self.clearScreen()
                turnStage = -1
            else:
                print("Invalid Input", end = "\n\n")

    def aiTurn(self, player):
        # Call stage One
        player.aiController.aiTurnStageOne(self.allResearch, self.board)

        # Carryout AI Choices
        if player.aiController.turnChoices.stageOne == 1:
            player.takeResearchCard()
        elif player.aiController.turnChoices.stageOne == 2:
            player.performResearch(player.aiController.turnChoices.researchChoice)
        elif player.aiController.turnChoices.stageOne == 3:
            self.reinforceTile(player, player.aiController.turnChoices.reinforcePos)

        player.aiController.aiTurnStageTwo()
        for moveOrder in player.aiController.turnChoices.moves:
            self.moveTroops(player, moveOrder.fromLocation, moveOrder.toLocation, moveOrder.troopsToMove)

        # (Un)comment line below to toggle display of board after AI Choices
        self.board.displayBoard()

        # (Un)comment line below to toggle turn by turn progress pauses
        input("Press space")

        if (self.debug):
            self.writeTurnToCSV(player)

    ### Spawn troops to given location based on reinforcement research
    def reinforceTile(self, player, location):
        boardGrid = self.board.boardGrid
        boardGrid[location[0]][location[1]].addTroops(player.getReinforcements(), player.color)

    ### Move troops given from and to location as well as number to move
    # TODO refactor into board
    def moveTroops(self, player, fromLocation, toLocation, troopsToMove):
        boardGrid = self.board.boardGrid
        # End location contains an army
        if boardGrid[toLocation[0]][toLocation[1]].color != TeamColor.NONE:
            # End location is friendly army
            if boardGrid[toLocation[0]][toLocation[1]].color == player.color:
                boardGrid[fromLocation[0]][fromLocation[1]].removeTroops(troopsToMove)
                boardGrid[toLocation[0]][toLocation[1]].addTroops(troopsToMove, player.color)
            # End location is enemy army
            else:
                boardGrid[fromLocation[0]][fromLocation[1]].removeTroops(troopsToMove)
                attackPower = player.research.attackResearch * troopsToMove
                if attackPower >=  boardGrid[toLocation[0]][toLocation[1]].troopCount:
                    boardGrid[toLocation[0]][toLocation[1]].removeTroops(boardGrid[toLocation[0]][toLocation[1]].troopCount)
                if troopsToMove > boardGrid[toLocation[0]][toLocation[1]].troopCount:
                    troopsLeft = troopsToMove - boardGrid[toLocation[0]][toLocation[1]].troopCount
                    if boardGrid[toLocation[0]][toLocation[1]].isBase:
                        self.killPlayer(boardGrid[toLocation[0]][toLocation[1]].color)
                        self.board.baseCapture(boardGrid[toLocation[0]][toLocation[1]].color, player.color)
                        player.victoryPoints += 3
                    boardGrid[toLocation[0]][toLocation[1]].addTroops(troopsLeft, player.color)
        # End location does not contain an army
        else:
            boardGrid[fromLocation[0]][fromLocation[1]].removeTroops(troopsToMove)
            boardGrid[toLocation[0]][toLocation[1]].addTroops(troopsToMove, player.color)

    # TODO Refactor Human interface to board
    def processGridInput(self, selectedSquareOne, selectedSquareTwo, player, forReinforcement, forAttack, forMovement):
        success = False
        boardGrid = self.board.boardGrid

        # Set square One
        rowLetterOne = selectedSquareOne[0].upper()
        rowLetterOne = ord(rowLetterOne)
        # 65 is the ascii for 'A' therefore remove 65 from letter to find proper row
        rowNumberOne = rowLetterOne - 65
        columnNumberOne = int(selectedSquareOne[1]) - 1

        # Set square Two
        rowLetterTwo = selectedSquareTwo[0].upper()
        rowLetterTwo = ord(rowLetterTwo)
        # 65 is the ascii for 'A' therefore remove 65 from letter to find proper row
        rowNumberTwo = rowLetterTwo - 65
        columnNumberTwo = int(selectedSquareTwo[1]) - 1

        # If selection is on board
        if (rowNumberOne >= 0 and rowNumberOne <= 9 and columnNumberOne >= 0 and columnNumberOne <= 9 and
                rowNumberTwo >= 0 and rowNumberTwo <= 9 and columnNumberTwo >= 0 and columnNumberTwo <= 9):

            # If location selection is for placing new troops
            if forReinforcement:
                if (boardGrid[rowNumberOne][columnNumberOne].color == player.color and
                        boardGrid[rowNumberOne][columnNumberOne].isBase and 
                        boardGrid[rowNumberOne][columnNumberOne].troopCount < (25 - player.getReinforcements())):
                    boardGrid[rowNumberOne][columnNumberOne].addTroops(player.getReinforcements(), player.color)
                    success = True
                else:
                    print("The provided space cannot take reinforcements. Please choose a different space.")

            # If locations are selected to attack
            elif forAttack:
                valid = False
                done = False
                if (boardGrid[rowNumberOne][columnNumberOne].color == player.color and
                       boardGrid[rowNumberTwo][columnNumberTwo].color != player.color and
                       boardGrid[rowNumberTwo][columnNumberTwo].getTroopCount > 0):
                    if (rowNumberTwo == rowNumberOne + 1 or rowNumberTwo == rowNumberOne - 1):
                        valid = True
                    elif (rowNumberTwo == rowNumberOne):
                        if (columnNumberTwo == columnNumberOne + 1 or columnNumberTwo == columnNumberOne - 1):
                            valid = True
                    else:
                        print("Locations are not adjacent to each other.")
                    while valid and not done:
                        print("You have {} troops available to attack.".format(boardGrid[rowNumberOne][columnNumberOne].troopCount))
                        troopsToAttack = input("How many troops would you like to order to attack? ")
                        troopsToAttack = int(troopsToAttack)
                        if troopsToAttack <= boardGrid[rowNumberOne][columnNumberOne].troopCount and troopsToAttack > 0:
                            boardGrid[rowNumberOne][columnNumberOne].removeTroops(troopsToAttack)
                            if(troopsToAttack <= boardGrid[rowNumberTwo][columnNumberTwo].troopCount):
                                boardGrid[rowNumberTwo][columnNumberTwo].removeTroops(troopsToAttack)
                            else:
                                boardGrid[rowNumberTwo][columnNumberTwo].removeTroops(boardGrid[rowNumberTwo][columnNumberTwo].troopCount)
                                boardGrid[rowNumberTwo][columnNumberTwo].addTroops(troopsToMove - boardGrid[rowNumberTwo][columnNumberTwo].troopCount)
                                if boardGrid[rowNumberTwo][columnNumberTwo].isBase:
                                    self.killPlayer(boardGrid[rowNumberTwo][columnNumberTwo].color)
                                    self.board.baseCapture(boardGrid[rowNumberTwo][columnNumberTwo].color, player.color)
                                    player.victoryPoints += 3
                            done = True
                            success = True
                        else:
                            print("Invalid Troop Number.")

            # If locations are selected for movement
            elif forMovement:
                valid = False
                done = False
                if (boardGrid[rowNumberOne][columnNumberOne].color == player.color):
                    if (rowNumberTwo == rowNumberOne + 1 or rowNumberTwo == rowNumberOne - 1):
                        valid = True
                    elif (rowNumberTwo == rowNumberOne):
                        if (columnNumberTwo == columnNumberOne + 1 or columnNumberTwo == columnNumberOne - 1):
                            valid = True
                    else:
                        print("Locations are not adjacent to each other.")
                    while valid and not done:
                        print("You have {} troops to move.".format(boardGrid[rowNumberOne][columnNumberOne].troopCount))
                        troopsToMove = input("How many troops would you like to move? ")
                        troopsToMove = int(troopsToMove)
                        if troopsToMove <= boardGrid[rowNumberOne][columnNumberOne].troopCount and troopsToMove > 0:
                            boardGrid[rowNumberOne][columnNumberOne].removeTroops(troopsToMove)
                            boardGrid[rowNumberTwo][columnNumberTwo].addTroops(troopsToMove, player.color)
                            done = True
                            success = True
                        else:
                            print("Invalid Troop number.")

        # Else location is not on board
        else:
            print("Invalid Input")
        return success

    ### Removes player from game from given color
    def killPlayer(self, color):
        if color == TeamColor.RED:
            self.redPlayer.isAlive = False
        elif color == TeamColor.BLUE:
            self.bluePlayer.isAlive = False
        elif color == TeamColor.YELLOW:
            self.yellowPlayer.isAlive = False
        else:
            self.greenPlayer.isAlive = False
            
    ### Outputs the turn information to the output CSV
    def writeTurnToCSV(self, player):
        i = 1
        with open('turn_Output.csv', mode='a') as turnOutput:
            turnWriter = csv.writer(turnOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            turnWriter.writerow([self.turnNumber, player.color.name, player.aiController.personality.name, player.aiController.myArmy,
                                 player.aiController.research.deploymentResearch, player.aiController.research.attackResearch,
                                 player.aiController.research.recruitmentResearch, player.aiController.research.researchPoints,
                                 player.aiController.turnChoices.stageOne, player.aiController.turnChoices.researchChoice,
                                 player.aiController.turnChoices.reinforcePos, player.aiController.turnChoices.numberOfMoves, player.victoryPoints])
            for move in player.aiController.turnChoices.moves:
                turnWriter.writerow(["", i, move.goalStatement.name, move.fromLocation, move.toLocation, move.troopsToMove])
                i = i + 1
