from enum import Enum


class SquareType(Enum):
    NONE = 0
    REGULAR = 1
    TRAP = 2
    LIVING = 3
    CELLAR = 4
    LABORATORY = 5
    PANTHEON = 6
    LIBRARY = 7
    GARAGE = 8
    BEDROOM = 9
    DINING = 10
    BAT = 11
    COBRA = 12
    SCORPION = 13
    SPIDER = 14


class Square:

    def __init__(self, squaretype: SquareType):
        self.squaretype = squaretype

    def __str__(self):
        return (str(self.squaretype.name)).lower().title()
