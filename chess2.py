from math import copysign

class Board:

    def __init__(self):
        pass

    def free(rank, file):
        for piece in pieces:
            if piece.rank == rank and piece.file == file:
                return piece
    
    def enpassant(rank, file):
        pass

class Scanner:

    def __init__(self, rank, file):
        self.rank = rank
        self.file = file

class Piece:

    def __init__(self, rank, file, colour):
        self.rank = rank
        self.file = file
        self.colour = colour

    def move(self, rank, file):
        if self.canmove(rank, file):
            self.rank = rank
            self.file = file
            if type(self) is Pawn and abs(rank - self.rank) == 2:
                return True
    
    def take(self):
        for piece in pieces.copy():
            if piece.rank == self.rank and piece.file == self.file and piece != self:
                pieces.remove(piece)
    
    def canmove(self, rank, file):
        other = Board.free(rank, file)
        if other is None:
            return True
        elif other.colour != self.colour:
            return True
        else:
            return False
        
class Bishop(Piece):

    def canmove(self, rank, file):
        if abs(self.rank - rank) != abs(self.file - file):
            return False
        else:
            scanner = Scanner(self.rank, self.file)
            for i in range(1, abs(rank - self.rank)):
                scanner.rank = self.rank + copysign(i, rank - self.rank)
                scanner.file = self.file + copysign(i, file - self.file)
                if Board.free(scanner.rank, scanner.file) is not None:
                    return False
        return Piece.canmove(self, rank, file)

class Rook(Piece):

    def canmove(self, rank, file):
        if self not in pieces:
            return False
        if (self.rank == rank) + (self.file == file) != 1:
            return False
        else:
            scanner = Scanner(self.rank, self.file)
            squares = max(abs(rank - self.rank), abs(file - self.file))
            for i in range(1, squares):
                scanner.rank = self.rank + i * (rank - self.rank) / squares
                scanner.file = self.file + i * (file - self.file) / squares
                if Board.free(scanner.rank, scanner.file) is not None:
                    return False
        return Piece.canmove(self, rank, file)

class Queen(Piece):

    def canmove(self, rank, file):
        if (self.rank == rank) + (self.file == file) == 1:
            scanner = Scanner(self.rank, self.file)
            squares = max(abs(rank - self.rank), abs(file - self.file))
            for i in range(1, squares):
                scanner.rank = self.rank + i * (rank - self.rank) / squares
                scanner.file = self.file + i * (file - self.file) / squares
                if Board.free(scanner.rank, scanner.file) is not None:
                    return False
            return Piece.canmove(self, rank, file)
        elif abs(rank - self.rank) == abs(file - self.file):
            scanner = Scanner(self.rank, self.file)
            for i in range(1, abs(rank - self.rank)):
                scanner.rank = self.rank + copysign(i, rank - self.rank)
                scanner.file = self.file + copysign(i, file - self.file)
                if Board.free(scanner.rank, scanner.file) is not None:
                    return False
            return Piece.canmove(self, rank, file)
        else:
            return False

class King(Piece):

    def check(self):
        for piece in pieces:
            if piece.canmove(self.rank, self.file) and piece.colour != self.colour:
                print("Check.")
                return True
        return False
        
    def canmove(self, rank, file):
        if rank - self.rank in [-1, 0, 1] and file - self.file in [-1, 0, 1] and (self.rank, self.file) != (rank, file):
            return Piece.canmove(self, rank, file)
        return False

class Knight(Piece):

    def canmove(self, rank, file):
        if abs((self.file - file) * (self.rank - rank)) != 2:
            return False
        return Piece.canmove(self, rank, file)

class Pawn(Piece):

    def canmove(self, rank, file):
        if self.colour == "W":
            if rank - self.rank == 1 and file - self.file == 0:
                return Board.free(rank, file) is None
            if rank == 3 and file - self.file == 0 and self.rank == 1:
                    return Board.free(rank, file) is None and Board.free(rank - 1, file) is None
            if rank - self.rank == 1 and abs(file - self.file) == 1:
                if Board.free(rank, file) is None:
                    if Board.enpassant(rank - 1, file):
                        return True
                    return False
                else:
                    return Piece.canmove(self, rank, file)
            return False
        if self.colour == "B":
            if rank - self.rank == -1 and file - self.file == 0:
                return Board.free(rank, file) is None
            if rank == 4 and file - self.file == 0 and self.rank == 6:
                    return Board.free(rank, file) is None and Board.free(rank + 1, file) is None
            if rank - self.rank == -1 and abs(file - self.file) == 1:
                if Board.free(rank, file) is None:
                    if Board.enpassant(rank + 1, file):
                        return True
                    return False
                else:
                    return Piece.canmove(self, rank, file)
            return False


def find_moves(list, rank, file):
    counter = 0
    captured = Board.free(rank, file)
    for i in list:
        if i.canmove(rank, file):
            origin = [i.rank, i.file].copy()
            i.move(rank, file)
            if captured is not None:
                i.take()
            if tomove == "W" and k1.check() or tomove == "B" and k2.check():
                i.rank = origin[0]
                i.file = origin[1]
                if captured is not None:
                    pieces.append(captured)
            else:
                counter += 1
    if counter != 1:
        print(counter)
        return True
    else:
        return False


def move_to_square(piece, rank, file):
    if piece == "K":
        if tomove == "W":
            illegal = find_moves([k1], rank, file)
        else:
            illegal = find_moves([k2], rank, file)
    elif piece == "Q":
        candidates = [q for q in queens if q.canmove(rank, file)]
        illegal = find_moves(candidates, rank, file)
    elif piece == "B":
        candidates = [b for b in bishops if b.canmove(rank, file)]
        illegal = find_moves(candidates, rank, file)
    elif piece == "N":
        candidates = [n for n in knights if n.canmove(rank, file)]
        illegal = find_moves(candidates, rank, file)
    elif piece == "R":
        candidates = [r for r in rooks if r.canmove(rank, file)]
        illegal = find_moves(candidates, rank, file)
    else:
        illegal = True
    return illegal


def next(tomove):
    if tomove == "W":
        return "B"
    else:
        return "W"


def repetition():
    pos = ""
    for piece in pieces:
        pos += str(type(piece)) + str(piece.rank) + str(piece.file)
    if hash(pos) not in positions:
        positions[hash(pos)] = 1
    else:
        positions[hash(pos)] += 1
        if positions[hash(pos)] == 3:
            return True
    return False

b1 = Bishop(0, 2, "W")
b2 = Bishop(0, 5, "W")
b3 = Bishop(7, 2, "B")
b4 = Bishop(7, 5, "B")
r1 = Rook(0, 0, "W")
r2 = Rook(0, 7, "W")
r3 = Rook(7, 0, "B")
r4 = Rook(7, 7, "B")
q1 = Queen(0, 3, "W")
q2 = Queen(7, 3, "B")
k1 = King(0, 4, "W")
k2 = King(7, 4, "B")
n1 = Knight(0, 1, "W")
n2 = Knight(0, 6, "W")
n3 = Knight(7, 1, "B")
n4 = Knight(7, 6, "B")
p1 = Pawn(1, 0, "W")
p2 = Pawn(1, 1, "W")
p3 = Pawn(1, 2, "W")
p4 = Pawn(1, 3, "W")
p5 = Pawn(1, 4, "W")
p6 = Pawn(1, 5, "W")
p7 = Pawn(1, 6, "W")
p8 = Pawn(1, 7, "W")
p9 = Pawn(6, 0, "B")
p10 = Pawn(6, 1, "B")
p11 = Pawn(6, 2, "B")
p12 = Pawn(6, 3, "B")
p13 = Pawn(6, 4, "B")
p14 = Pawn(6, 5, "B")
p15 = Pawn(6, 6, "B")
p16 = Pawn(6, 7, "B")

pieces = [b1, b2, b3, b4 ,r1, r2, r3, r4, q1, q2, k1, k2, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, n1, n2, n3, n4]
hasmoved = set()
positions = {}
move50 = -1
tomove = "W"

def display():
    sahovnica = []
    for i in range(8):
        row = []
        for j in range(8):
            piece = Board.free(i, j)
            if piece is None:
                row.append(" ")
            else:
                if type(piece) is Pawn:
                    row.append("P") if piece.colour == "W" else row.append("p")
                elif type(piece) is Rook:
                    row.append("R") if piece.colour == "W" else row.append("r")
                elif type(piece) is Knight:
                    row.append("N") if piece.colour == "W" else row.append("n")
                elif type(piece) is Bishop:
                    row.append("B") if piece.colour == "W" else row.append("b")
                elif type(piece) is Queen:
                    row.append("Q") if piece.colour == "W" else row.append("q")
                elif type(piece) is King:
                    row.append("K") if piece.colour == "W" else row.append("k")
                else:
                    row.append("?")
                    print("There is an impostor among us.")
        sahovnica.append(row)
    return sahovnica


while True:
    pawns = [p for p in pieces if type(p) is Pawn and p.colour == tomove]
    queens = [q for q in pieces if type(q) is Queen and q.colour == tomove]
    bishops = [b for b in pieces if type(b) is Bishop and b.colour == tomove]
    knights = [n for n in pieces if type(n) is Knight  and n.colour == tomove]
    rooks = [r for r in pieces if type(r) is Rook and r.colour == tomove]
    illegal = False
    captured = None

    if tomove == "W":
        for i in display()[::-1]:
            print(i)
        move = input("White to move: ")
    else:
        for i in display():
            print(i[::-1])
        move = input("Black to move: ")

    if move == "#":
        if tomove == "W":
            print("Game over, black wins!")
        else:
            print("Game over, white wins!")
        break

    elif len(move) == 2 or len(move) == 3 and move[2] in "+#":

        if move[0] not in "abcdefgh" or move[1] not in "1234567":
            illegal = True
        else:
            rank = int(move[1]) - 1
            file = ord(move[0]) - 97
            illegal = find_moves(pawns, rank, file)
            if not illegal:
                move50 = -1
                positions = {}

    elif len(move) == 3 or len(move) == 4 and move[3] in "+#":

        if move[1] in "abcdefgh" or move[2] in "12345678":
            rank = int(move[2]) - 1
            file = ord(move[1]) - 97
            if Board.free(rank, file) is not None:
                illegal = True
            else:
                illegal = move_to_square(move[0], rank, file)

        elif move == "0-0":
            if tomove == "W" and k1 not in hasmoved and r2 not in hasmoved and r2.canmove(0, 5):
                illegal = find_moves([k1], 0, 5)
                if not illegal:
                    illegal = find_moves([k1], 0, 6)
                    if not illegal:
                        r2.file = 5
            elif k2 not in hasmoved and r4 not in hasmoved:
                if r4.canmove(7, 5):
                    illegal = find_moves([k2], 7, 5)
                    if not illegal:
                        illegal = find_moves([k2], 7, 6)
                        if not illegal:
                            r4.file = 5
                        else:
                            k2.file = 4
            else:
                illegal = True
        
        else:
            illegal = True

    elif len(move) == 4 or len(move) == 5 and move[4] in "+#":

        if move[0] in "abcdefgh" and move[1] == "8" and move[2] == "=":
            file = ord(move[0]) - 97
            illegal = find_moves(pawns, 8, file)
            for pawn in pawns.copy():
                if pawn.rank == 7:
                    if move[3] == "R":
                        rook = Rook(7, file, tomove)
                        pieces.remove(pawn)
                        pieces.append(rook)
                    elif move[3] == "N":
                        knight = Knight(7, file, tomove)
                        pieces.remove(pawn)
                        pieces.append(knight)
                    elif move[3] == "B":
                        bishop = Bishop(7, file, tomove)
                        pieces.remove(pawn)
                        pieces.append(knight)
                    elif move[3] == "Q":
                        queen = Queen(7, file, tomove)
                        pawn.move(7, file)
                        pieces.remove(pawn)
                        pieces.append(queen)
                    else:
                        illegal = True

        elif move[1] == "x" and move[2] in "abcdefgh" and move[3] in "12345678":
            rank = int(move[3]) - 1
            file = ord(move[2]) - 97
            if Board.free(rank, file) is None:
                illegal = True
            else:
                if move[0] in "abcdefgh":
                    illegal = find_moves(pawns, rank, file)
                else:
                    illegal = move_to_square(move[0], rank, file)
            if not illegal:
                move50 = -1
                positions = {}

        elif move[0] in "BRQN" and move[2] in "abcdefgh" and move[3] in "12345678":
            rank = int(move[3]) - 1
            file = ord(move[2]) - 97
            options = []
            if move[0] == "Q":
                candidates = queens
            if move[0] == "B":
                candidates = bishops
            if move[0] == "N":
                candidates = knights
            if move[0] == "R":
                candidates = rooks
            if move[1] in "abcdefgh":
                options = [piece for piece in candidates if piece.file == ord(move[1]) - 97]
            elif move[1] in "12345678":
                options = [piece for piece in candidates if piece.rank == int(move[1]) - 1]
            illegal = find_moves(options, rank, file)

        else:
            illegal = True

    elif len(move) == 5 or len(move) == 6 and move[5] in "+#":

        if move[2] == "x" or move[3] in "abcdefgh" or move[4] in "12345678":
            rank = int(move[4]) - 1
            file = ord(move[3]) - 97
            if Board.free(rank, file) is None:
                illegal = True
            else:
                options = []
                if move[0] == "Q":
                    candidates = queens
                if move[0] == "B":
                    candidates = bishops
                if move[0] == "N":
                    candidates = knights
                if move[0] == "R":
                    candidates = rooks
                if move[1] in "abcdefgh":
                    options = [piece for piece in candidates if piece.file == ord(move[1]) - 97]
                elif move[1] in "12345678":
                    options = [piece for piece in candidates if piece.file == int(move[1]) - 1]
                illegal = find_moves(options, rank, file)
            if not illegal:
                move50 = -1
                positions = {}

        elif move[0] in "QBNR" and all(x in "abcdefgh" for x in [move[1], move[3]]) and all(x in "12345678" for x in [move[2], move[4]]):
            rank = int(move[4]) - 1
            file = ord(move[3]) - 97
            illegal = find_moves([q for q in queens if q.file == ord(move[1]) and q.rank == int(move[2])], rank, file)
        
        elif move == "0-0-0":
            if tomove == "W" and k1 not in hasmoved and r1 not in hasmoved and r1.canmove(0, 3):
                illegal = find_moves([k1], 0, 3)
                if not illegal:
                    illegal = find_moves([k1], 0, 2)
                    if not illegal:
                        r1.file = 3
                    else:
                        k1.file = 4
            elif k2 not in hasmoved and r3 not in hasmoved and r3.canmove(7, 3):
                illegal = find_moves([k2], 7, 3)
                if not illegal:
                    illegal = find_moves([k2], 7, 2)
                    if not illegal:
                        r3.file = 3
                    else:
                        k1.file = 4

        else:
            illegal = True

    elif len(move) == 6 or len(move) == 7 and move[6] in "+#" and "x" in move:

        split = move.split("x")
        if split[1][0] not in "abcdefgh" or split[1][1] not in "12345678" or Board.free(rank, file) is None:
            illegal = True
        else:
            rank = int(split[1][1]) - 1
            file = ord(split[1][0]) - 97

            if move in "abcdefgh" and move[5] == "=":
                illegal = find_moves(pawns, rank, file)
                for pawn in pawns.copy():
                    if pawn.rank == 7:
                        if move[3] == "R":
                            rook = Rook(7, file, tomove)
                            pieces.remove(pawn)
                            pieces.append(rook)
                        elif move[3] == "N":
                            knight = Knight(7, file, tomove)
                            pieces.remove(pawn)
                            pieces.append(knight)
                        elif move[3] == "B":
                            bishop = Bishop(7, file, tomove)
                            pieces.remove(pawn)
                            pieces.append(knight)
                        elif move[3] == "Q":
                            queen = Queen(7, file, tomove)
                            pawn.move(7, file)
                            pieces.remove(pawn)
                            pieces.append(queen)
                        else:
                            illegal = True

            elif move[0] in "QBNR" and move[1] in "abcdefgh" and move[2] in "12345678":
                illegal = find_moves([q for q in queens if q.file == ord(move[1]) and q.rank == int(move[2])], rank, file)
            
            else:
                illegal = True
        
        if not illegal:
            move50 = -1
            positions = {}

    else:
        illegal = True

    tomove = next(tomove)
    if illegal:
        print("Illegal move or invalid notation.")
        tomove = next(tomove)
    else:
        piece = Board.free(rank, file)
        hasmoved.add(piece)
        if repetition():
            print("Draw by repetition.")
            break
        move50 += 1
        if move50 == 100:
            print("Draw by 50 move rule.")
            break
