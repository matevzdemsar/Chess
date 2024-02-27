from math import copysign

class Piece:

    def __init__(self, rank, file, colour):
        self.rank = rank
        self.file = file
        self.colour = colour
    
    def can_move(self, rank, file):
        if self.colour != tomove:
            print("Colour")
            return False
        else:
            target = Board.occ(rank, file)
            if not target:
                return True
            else:
                print("Occupied")
                return target.colour != self.colour
    
    def move(self, rank, file):
        self.rank = rank
        self.file = file

class Knight(Piece):
    
    def can_move(self, rank, file):
        if abs((rank - self.rank) * (file - self.file)) != 2:
            return False
        else:
            return Piece.can_move(rank, file)

class Bishop(Piece):
    
    def can_move(self, rank, file):
        if abs(rank - self.rank) != abs(file - self.file):
            return False
        else:
            for i in range(1, abs(rank - self.rank)):
                square = Board.occ(self.rank + copysign(i, rank - self.rank), self.file + copysign(i, file - self.file))
                if square:
                    return False
            return Piece.can_move(self, rank, file)

class Rook(Piece):
    
    def can_move(self, rank, file):
        if (self.rank == rank) + (self.file == file) != 1:
            return False
        else:
            dist = max(abs(self.file - file), abs(self.rank - rank))
            for i in range(1, dist):
                square = Board.occ(self.rank + i * (rank - self.rank) / dist, self.file + i * (file - self.file) / dist)
                if square:
                    return False
            return Piece.can_move(self, rank, file)

class Queen(Piece):
    
    def can_move(self, rank, file):
        if abs(rank - self.rank) != abs(file - self.file) and (self.rank == rank) + (self.file == file) != 1:
            return False
        else:
            dist = max(abs(self.file - file), abs(self.rank - rank))
            for i in range(1, dist):
                square = Board.occ(self.rank + i * (rank - self.rank) / dist, self.file + i * (file - self.file) / dist)
                if square:
                    return False
            return Piece.can_move(self, rank, file)
            
        
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

tomove = True
pieces = []
