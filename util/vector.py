# Needed to use typing of the enclosing class
from __future__ import annotations


class Vector2d:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def non_diagonal_distance_to(self, other: Vector2d):
        dist1 = abs(self.x - other.x)
        dist2 = abs(self.y - other.y)
        return dist1 + dist2

    def add(self, x = 0, y = 0):
        self.x += x
        self.y += y
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'
