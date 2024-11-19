from enum import Enum


class CellType(Enum):
    Empty = 1
    Wall = 2


class CellMark(Enum):
    No = 0
    Start = 1
    End = 2


class ArrowDirection(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


class Mode(Enum):
    Cost = 1
    Arrow = 2


class HeuristicType(Enum):
    MANHATTAN = 0
    EUCLIDEAN = 1
    COMBINED = 2
