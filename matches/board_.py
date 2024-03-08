from .square import Square, SquareType
from typing import List
from util.vector import Vector2d


class Board:

    WIDTH = 20
    HEIGHT = 20

    TRAPS = [(6, 6), (13, 6), (6, 13), (13, 13)]

    BAT = [(6, 5), (6, 15)]
    COBRA = [(3, 13), (14, 13)]
    SCORPION = [(13, 5), (13, 16)]
    SPIDER = [(15, 6), (4, 6)]

    ROOM_LIVING = [(3, 6), (6, 9), (4, 13)]
    ROOM_CELLAR = [(6, 4)]
    ROOM_LABORATORY = [(13, 3)]
    ROOM_PANTHEON = [(16, 6), (13, 9), (15, 13)]
    ROOM_LIBRARY = [(13, 15)]
    ROOM_GARAGE = [(6, 17)]
    ROOM_BEDROOM = [(10, 13)]
    ROOM_DINING = [(10, 6)]

    def __init__(self, players: List[str]):
        self.STARTING_SQUARES = [(0, 6), (6, 0), (13, 0), (0, 13), (19, 6), (6, 19), (19, 13), (13, 19)]
        self.squares = []
        # {'player_name': Vector2d(x, y), ... }
        self.player_position = {}

        # Assign starting positions to players
        for p in players:
            self.player_position[p] = Vector2d(self.STARTING_SQUARES[0][0], self.STARTING_SQUARES[0][1])
            self.STARTING_SQUARES.pop(0)

        # Init board squares
        for i in range(0, self.WIDTH):
            sublist = []
            for j in range(0, self.HEIGHT):
                # Some coordinates aren't supposed to have squares in them, so we fill with None
                if (i < 6 or 6 < i < 13 or i > 13) and (j < 6 or 13 > j > 6 or j > 13):
                    sublist.append(Square(SquareType.NONE))
                else:
                    sublist.append(self.__get_room(i, j))
            self.squares.append(sublist)

    def __get_room(self, i, j):
        if (i, j) in self.ROOM_LIVING:
            room = Square(SquareType.LIVING)
        elif (i, j) in self.ROOM_BEDROOM:
            room = Square(SquareType.BEDROOM)
        elif (i, j) in self.ROOM_CELLAR:
            room = Square(SquareType.CELLAR)
        elif (i, j) in self.ROOM_LABORATORY:
            room = Square(SquareType.LABORATORY)
        elif (i, j) in self.ROOM_PANTHEON:
            room = Square(SquareType.PANTHEON)
        elif (i, j) in self.ROOM_LIBRARY:
            room = Square(SquareType.LIBRARY)
        elif (i, j) in self.ROOM_GARAGE:
            room = Square(SquareType.GARAGE)
        elif (i, j) in self.ROOM_DINING:
            room = Square(SquareType.DINING)
        elif (i, j) in self.TRAPS:
            room = Square(SquareType.TRAP)
        elif (i, j) in self.BAT:
            room = Square(SquareType.BAT)
        elif (i, j) in self.COBRA:
            room = Square(SquareType.COBRA)
        elif (i, j) in self.SCORPION:
            room = Square(SquareType.SCORPION)
        elif (i, j) in self.SPIDER:
            room = Square(SquareType.SPIDER)
        else:
            room = Square(SquareType.REGULAR)

        return room

    def move_player(self, position: Vector2d, player_name: str, moves: int) -> Square:
        player_pos = self.player_position[player_name]
        required_moves = player_pos.non_diagonal_distance_to(position)
        target_square = self.squares[position.x][position.y]
        trap_to_trap = target_square.squaretype is SquareType.TRAP and \
                       self.get_player_square(player_name).squaretype is SquareType.TRAP
        portal_to_portal = target_square.squaretype.value > 10 and \
                           self.get_player_square(player_name).squaretype.value > 10 and \
                            target_square.squaretype == self.get_player_square(player_name).squaretype

        if required_moves > moves and not trap_to_trap and not portal_to_portal:
            raise Exception(f'Target square is too far away moves: {moves}, moves required: {required_moves}')
        if self.squares[position.x][position.y].squaretype is SquareType.NONE:
            raise Exception('Selected square is not suitable')
        # Make sure player doesn't move after jumping through a trap
        if trap_to_trap:
            required_moves = moves
        # Player can keep on moving after jumping through a portal
        elif portal_to_portal:
            required_moves = 0

        self.player_position[player_name] = position

        return moves - required_moves

    def get_player_position(self, player_name) -> Vector2d:
        return self.player_position[player_name]

    def get_player_square(self, player_name) -> Square:
        p = self.player_position[player_name]
        return self.squares[p.x][p.y]

    def to_dict(self):
        return {'board': [[str(b2) for b2 in b] for b in self.squares],
                'player_position': [{'pos_x': v.x, 'pos_y': v.y} for v in self.player_position]}

    def positions_to_dict(self):
        return {'player_position': [{'pos_x': self.player_position[v].x,
                                     'pos_y': self.player_position[v].y,
                                     'player_name': v} for v in self.player_position]}
