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



def board_to_pieces(board):
    pieces = []
    for i in board:
        for j in i:
            if j != " ":
                piece = [King, Pawn, Knight, Bishop, Rook, Queen][j in "Pp" + \
                2 * j in "Nn" + 3 * j in "Bb" + 4 * j in "Rr" + 5 * j in "Qq"]
                pieces.append(piece(i, j, j.isupper()))
    return pieces


def pieces_to_board():
    board = []
    for i in range(8):
        row = []
        for j in range(8):
            piece = Board.occ(i, j)
            if not piece:
                row.append(" ")
            else:
                t = type(piece)
                symb = "kpnrb"[t is Pawn + 2 * t is Knight + 3 * t is Rook + 4 * t is Queen]
                if piece.colour:
                    row.append(symb.upper())
                else:
                    row.append(symb)
        board.append(row)


def castles(colour, side):
    king = kings[colour]
    rook = rooks[colour][side]
    if king.has_moved or rook.has_moved:
        return False
    elif not rook.canmove(self.rank, king.file + 2 * side - 1):
        return False
    else:
        king.file += 2 * side - 1
        if not is_legal(pieces, colour):
            king.file -= 2 * side - 1
            return False
        king.file += 2 * side - 1
        if not is_legal(pieces, colour):
            king.file -= 4 * side - 2
            return False
        rook.move(self.rank, king.file - 2 * side + 1)
        king.has_moved = True


b1 = Bishop(0, 2, True)
b2 = Bishop(0, 5, True)
b3 = Bishop(7, 2, False)
b4 = Bishop(7, 5, False)
r1 = Rook(0, 0, True)
r2 = Rook(0, 7, True)
r3 = Rook(7, 0, False)
r4 = Rook(7, 7, False)
q1 = Queen(0, 3, True)
q2 = Queen(7, 3, False)
k1 = King(0, 4, True)
k2 = King(7, 4, False)
n1 = Knight(0, 1, True)
n2 = Knight(0, 6, True)
n3 = Knight(7, 1, False)
n4 = Knight(7, 6, False)
p1 = Pawn(1, 0, True)
p2 = Pawn(1, 1, True)
p3 = Pawn(1, 2, True)
p4 = Pawn(1, 3, True)
p5 = Pawn(1, 4, True)
p6 = Pawn(1, 5, True)
p7 = Pawn(1, 6, True)
p8 = Pawn(1, 7, True)
p9 = Pawn(6, 0, False)
p10 = Pawn(6, 1, False)
p11 = Pawn(6, 2, False)
p12 = Pawn(6, 3, False)
p13 = Pawn(6, 4, False)
p14 = Pawn(6, 5, False)
p15 = Pawn(6, 6, False)
p16 = Pawn(6, 7, False)

pieces = [b1, b2, b3, b4 ,r1, r2, r3, r4, q1, q2, k1, k2, p1, p2, p3, \
p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, n1, n2, n3, n4]
kings = [k2, k1]
rooks = [[r4, r3][r2, r1]]
tomove = True
