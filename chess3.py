from math import copysign

class Board:

    def __init__(self):
        pass

    def occ(rank, file):
        for piece in pieces:
            if piece.rank == rank and piece.file == file:
                return piece
        return False

    def take(rank, file):
        for piece in pieces.copy():
            if piece.rank == rank and piece.file == file:
                pieces.remove(piece)

class Piece:

    def __init__(self, rank, file, colour):
        self.rank = rank
        self.file = file
        self.colour = colour
    
    def move(self, rank, file):
        self.rank = rank
        self.file = file

    def canmove(rank, file):
        if rank not in range(8) or file not in range(8):
            return False

pieces = []