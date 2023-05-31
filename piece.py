from __future__ import annotations

from typing import TYPE_CHECKING

from const import BLACK, WHITE, COLOR, Empty, Coord
from move import Move

if TYPE_CHECKING:
    from game import Game


class Piece(Empty):
    movement: tuple[Coord]
    notation: str

    def __init__(self, side: WHITE | BLACK, game: Game):
        self.side = side
        self.game = game

    def __bool__(self):
        return True

    def moves(self, coord):
        for vector in self.movement:
            if (target := coord + vector):
                piece = self.game.get(target)
                if not piece or self.side != piece.side:
                    yield Move(self, coord, target)

    def controls(self, coord):
        for vector in self.movement:
            if (target := coord + vector):
                yield target


class Pawn(Piece):
    char = "P"
    notation = ""

    def __init__(self, side: WHITE | BLACK, game: Game):
        super().__init__(side, game)
        if side:
            self.vector = Coord(0, 1)
            self.start = 1
            self.promotion = 7
            self.capture = Coord(-1, 1), Coord(1, 1)
        else:
            self.vector = Coord(0, -1)
            self.start = 6
            self.promotion = 0
            self.capture = Coord(1, -1), Coord(1, -1)

    def moves(self, coord: Coord):
        for vector in self.capture:
            if (target := coord + vector):
                piece = self.game.get(target)
                if piece and self.side != piece.side:
                    move = Move(self, coord, target)
                    if target.y == self.promotion:
                        move.new = True
                    yield move

        if (target := coord + self.vector):
            if not self.game.get(target):
                move = Move(self, coord, target)
                if target.y == self.promotion:
                    move.new = True
                yield move
                if coord.y == self.start:
                    target += self.vector
                    if not self.game.get(target):
                        yield Move(self, coord, target, target)

        if (p := self.game.en_passant):
            if coord.y == p.y and (coord.x - 1 == p.x or coord.x + 1 == p.x):
                yield Move(
                    self, coord, p + self.vector, empty=self.game.en_passant
                )

    def controls(self, coord):
        for vector in self.capture:
            if (target := coord + vector):
                yield target


class Knight(Piece):
    movement = (
        Coord(2, 1), Coord(1, 2), Coord(-1, 2), Coord(-2, 1),
        Coord(-2, -1), Coord(-1, -2), Coord(1, -2), Coord(2, -1)
    )
    char = "N"
    notation = char


class Slide(Piece):
    def moves(self, coord):
        for vector in self.movement:
            for factor in range(1, 8):
                if (target := coord + vector * factor):
                    if (piece := self.game.get(target)):
                        if self.side != piece.side:
                            yield Move(self, coord, target)
                        break
                    yield Move(self, coord, target)

    def controls(self, coord):
        for vector in self.movement:
            for factor in range(1, 8):
                if (target := coord + vector * factor):
                    yield target
                    if self.game.get(target):
                        break


class Rook(Slide):
    moved: bool = False
    movement = Coord(0, 1), Coord(1, 0), Coord(-1, 0), Coord(0, -1)
    char = "R"
    notation = char


class Bishop(Slide):
    movement = Coord(1, 1), Coord(-1, 1), Coord(-1, -1), Coord(1, -1) 
    char = "B"
    notation = char


class Queen(Slide):
    movement = (
        Coord(0, 1), Coord(1, 1), Coord(1, 0), Coord(-1, 1),
        Coord(-1, 0), Coord(-1, -1), Coord(0, -1), Coord(1, -1)
    )
    char = "Q"
    notation = char


class King(Piece):
    moved: bool = False
    movement = (
        Coord(0, 1), Coord(1, 1), Coord(1, 0), Coord(-1, 1),
        Coord(-1, 0), Coord(-1, -1), Coord(0, -1), Coord(1, -1)
    )
    char = "K"
    notation = char

    def __init__(self, side: BLACK | WHITE, game: Game):
        super().__init__(side, game)
        if side:
            self.y = 0
        else:
            self.y = 7

    def moves(self, coord: Coord):
        for move in super().moves(coord):
            move.moved = True
            yield move

        if not self.moved and coord not in self.game.controls:
            rook = Coord(0, self.y)
            if not self.game.get(rook).moved:
                vector = Coord(-1, 0)
                for factor in range(1, 4):
                    square = coord + vector * factor
                    if self.game.get(square) or square in self.game.controls:
                        break
                else:
                    target = Coord(2, self.y)
                    yield Move(
                        self, coord, target, 
                        empty=rook, new=target-vector,
                        notation="0-0-0", moved=True
                    )

            rook = Coord(7, self.y)
            if not self.game.get(rook).moved:
                vector = Coord(1, 0)
                for factor in range(1, 3):
                    square = coord + vector * factor
                    if self.game.get(square) or square in self.game.controls:
                        break
                else:
                    target = Coord(6, self.y)
                    yield Move(
                        self, coord, target,
                        empty=rook, new=target-vector,
                        notation="0-0", moved=True
                    )

