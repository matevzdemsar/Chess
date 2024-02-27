from math import copysign

class Piece:

    def __init__(self, rank, file, colour):
        self.rank = rank
        self.file = file
        self.colour = colour
    
    def can_move(self, rank, file):
        if self.colour != tomove:
            return False
        else:
            target = Board.occ(rank, file)
            if not target:
                return True
            else:
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

class King(Piece):

    def can_move(self, rank, file):
        dy = abs(rank - self.rank)
        dx = abs(file - self.file)
        if dx in (0, 1) and dy in (0, 1) and dx + dy != 2:
            return Piece.can_move(self, rank, file)
        return False

class Pawn(Piece):

    def can_move(self, rank, file):
        if self.file == file:
            if rank == self.rank + 2 * tomove - 1:
                return Piece.can_move(self, rank, file)
            elif rank == self.rank + 4 * tomove - 2:
                if Board.occ(rank, file) or Board.occ(rank - 2 * tomove + 1, file) and self.rank not in (1, 6):
                    return False
                else:
                    en_passant = (self.rank + 2 * tomove + 1, file)
                    return True
        elif abs(self.file - file) == 1 and rank == self.rank + 2 * tomove - 1:
            target = Board.occ(rank, file)
            if target is not False:
                return target.colour != self.colour
            else:
                return rank, file == en_passant
        else:
            return False

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

p1 = Pawn(1, 4, True)
p2 = Pawn(3, 5, False)
en_passant = (-1, -1)
tomove = True
pieces = [p1, p2]
print(p1.can_move(3, 4))
p1.move(3, 4)
print(en_passant)
print(p2.can_move(2, 4))