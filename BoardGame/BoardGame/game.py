"""
Project Name: 
File Name: game.py
Author: Lex Hall
Last Updated: 
Python Version: 3.6
"""

from os import system, name
import time

import tile
import board
import player
import InfoObjects
from enums import *

class Game(object):
    def __init__(self):
        self.board = board.Board()
        self.redPlayer = player.PlayerInfo(TeamColor.RED)
        self.bluePlayer = player.PlayerInfo(TeamColor.BLUE)
        self.yellowPlayer = player.PlayerInfo(TeamColor.YELLOW)
        self.greenPlayer = player.PlayerInfo(TeamColor.GREEN)
        self.allResearch = InfoObjects.AllResearch()

    def play(self):
        self.assignAIPlayers(True)
        self.gameLoop()

    def assignAIPlayers(self, standard):
        if standard:
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
        
    def gameLoop(self):
        done = False
        winningPlayer = None
        while not done:
            if self.redPlayer.getIsAlive():
                self.board.applyAttrition(self.redPlayer)
                if self.redPlayer.getIsNPC():
                    self.aiTurn(self.redPlayer)
                else:
                    self.playerTurn(self.redPlayer)
                self.allResearch.redResearch = self.redPlayer.research
                if self.redPlayer.getHasWon():
                    done = True
                    winningPlayer = self.redPlayer
                    break

            if self.yellowPlayer.getIsAlive():
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

            if self.bluePlayer.getIsAlive():
                self.board.applyAttrition(self.bluePlayer)
                if self.bluePlayer.getIsNPC():
                    self.aiTurn(self.bluePlayer)
                else:
                    self.playerTurn(self.bluePlayer)
                self.allResearch.blueResearch = self.bluePlayer.research
                if self.bluePlayer.getHasWon():
                    done = True
                    winningPlayer = self.bluePlayer
                    break
                
            if self.greenPlayer.getIsAlive():
                self.board.applyAttrition(self.greenPlayer)
                if self.greenPlayer.getIsNPC():
                    self.aiTurn(self.greenPlayer)
                else:
                    self.playerTurn(self.greenPlayer)
                self.allResearch.greenResearch = self.greenPlayer.research
                if self.greenPlayer.getHasWon():
                    done = True
                    winningPlayer = self.greenPlayer
                
        
        # Victory
        self.clearScreen()
        print("Victory! Congratulations...")
        winningPlayer.displayName()

    # TODO refactor to AllResearch object
    def displayAllResearch(self):
        self.redPlayer.displayResearch(False, False)
        self.bluePlayer.displayResearch(False, False)
        self.yellowPlayer.displayResearch(False, False)
        self.greenPlayer.displayResearch(False, False)

    def clearScreen(self):
        if name == 'nt': 
            _ = system('cls')

        else:
            _ = system('clear')

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
                    if moves != player.getDeployment():
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
                    if moves != player.getDeployment():
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
        aiTurnInstructions = InfoObjects.AITurn()
        aiTurnInstructions = player.aiController.aiTurn(self.allResearch, self.board)
        print(player.aiController.personality.name)
        print(aiTurnInstructions.stageOne)
        print(aiTurnInstructions.researchChoice)
        print(aiTurnInstructions.reinforcePos)
        input("Press 'Enter' to end turn...")

    def processGridInput(self, selectedSquareOne, selectedSquareTwo, player, forReinforcement, forAttack, forMovement):
        success = False
        boardGrid = self.board.getBoardGrid()

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
                if (boardGrid[rowNumberOne][columnNumberOne].getTeamColor() == player.getTeamColor() and
                        boardGrid[rowNumberOne][columnNumberOne].getIsBase() and 
                        boardGrid[rowNumberOne][columnNumberOne].getTroopCount() < (25 - player.getReinforcements())):
                    boardGrid[rowNumberOne][columnNumberOne].addTroops(player.getReinforcements(), player.getTeamColor())
                    success = True
                else:
                    print("The provided space cannot take reinforcements. Please choose a different space.")

            # If locations are selected to attack
            elif forAttack:
                valid = False
                done = False
                if (boardGrid[rowNumberOne][columnNumberOne].getTeamColor() == player.getTeamColor() and
                       boardGrid[rowNumberTwo][columnNumberTwo].getTeamColor() != player.getTeamColor() and
                       boardGrid[rowNumberTwo][columnNumberTwo].getTroopCount > 0):
                    if (rowNumberTwo == rowNumberOne + 1 or rowNumberTwo == rowNumberOne - 1):
                        valid = True
                    elif (rowNumberTwo == rowNumberOne):
                        if (columnNumberTwo == columnNumberOne + 1 or columnNumberTwo == columnNumberOne - 1):
                            valid = True
                    else:
                        print("Locations are not adjacent to each other.")
                    while valid and not done:
                        print("You have {} troops available to attack.".format(boardGrid[rowNumberOne][columnNumberOne].getTroopCount()))
                        troopsToAttack = input("How many troops would you like to order to attack? ")
                        troopsToAttack = int(troopsToAttack)
                        if troopsToAttack <= boardGrid[rowNumberOne][columnNumberOne].getTroopCount() and troopsToAttack > 0:
                            boardGrid[rowNumberOne][columnNumberOne].removeTroops(troopsToAttack)
                            if(troopsToAttack <= boardGrid[rowNumberTwo][columnNumberTwo].getTroopCount()):
                                boardGrid[rowNumberTwo][columnNumberTwo].removeTroops(troopsToAttack)
                            else:
                                boardGrid[rowNumberTwo][columnNumberTwo].removeTroops(boardGrid[rowNumberTwo][columnNumberTwo].getTroopCount())
                                boardGrid[rowNumberTwo][columnNumberTwo].addTroops(troopsToMove - boardGrid[rowNumberTwo][columnNumberTwo].getTroopCount())
                                if boardGrid[rowNumberTwo][columnNumberTwo].getIsBase():
                                    self.killPlayer(boardGrid[rowNumberTwo][columnNumberTwo].getTeamColor())
                                    self.board.baseCapture(boardGrid[rowNumberTwo][columnNumberTwo].getTeamColor(), player.getTeamColor())
                                    player.gainCommandPoints(3)
                            done = True
                            success = True
                        else:
                            print("Invalid Troop Number.")

            # If locations are selected for movement
            elif forMovement:
                valid = False
                done = False
                if (boardGrid[rowNumberOne][columnNumberOne].getTeamColor() == player.getTeamColor()):
                    if (rowNumberTwo == rowNumberOne + 1 or rowNumberTwo == rowNumberOne - 1):
                        valid = True
                    elif (rowNumberTwo == rowNumberOne):
                        if (columnNumberTwo == columnNumberOne + 1 or columnNumberTwo == columnNumberOne - 1):
                            valid = True
                    else:
                        print("Locations are not adjacent to each other.")
                    while valid and not done:
                        print("You have {} troops to move.".format(boardGrid[rowNumberOne][columnNumberOne].getTroopCount()))
                        troopsToMove = input("How many troops would you like to move? ")
                        troopsToMove = int(troopsToMove)
                        if troopsToMove <= boardGrid[rowNumberOne][columnNumberOne].getTroopCount() and troopsToMove > 0:
                            boardGrid[rowNumberOne][columnNumberOne].removeTroops(troopsToMove)
                            boardGrid[rowNumberTwo][columnNumberTwo].addTroops(troopsToMove, player.getTeamColor())
                            done = True
                            success = True
                        else:
                            print("Invalid Troop number.")

        # Else location is not on board
        else:
            print("Invalid Input")
        return success

    def killPlayer(self, color):
        if color == TeamColor.RED:
            self.redPlayer.kill()
        elif color == TeamColor.BLUE:
            self.bluePlayer.kill()
        elif color == TeamColor.YELLOW:
            self.yellowPlayer.kill()
        else:
            self.greenPlayer.kill()
            
