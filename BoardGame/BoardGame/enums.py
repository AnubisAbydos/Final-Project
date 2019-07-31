"""
Project Name: BoardGame
File Name: enums.py
Author: Lex Hall
Last Updated: 7/29/19
Python Version: 3.6
"""

from enum import Enum

class TeamColor(Enum):
    NONE = 0
    RED = 1
    YELLOW = 2
    BLUE = 3
    GREEN = 4

''' ENUM RowAlpha
Stores the alpha to num conversions for interpeting board locations
'''
class RowAlpha(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9

class PersonalityTypes(Enum):
    Researcher = 0
    Turtle = 1
    CenterDom = 2
    BaseRusher = 3
    DefenseWebber = 4

class GoalStatement(Enum):
    NONE = 0
    CenterResearch = 1
    CenterVictory = 2
    DefenseLocation = 3
    BaseAttack = 4
    DoomStack = 5