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
            if self == Pawn and abs(rank - self.rank) == 2:
                return True
    
    def canmove(self, rank, file):
        if tomove != self.colour:
            return False
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
                print(scanner.rank, scanner.file)
                scanner.rank = self.rank + copysign(i, rank - self.rank)
                scanner.file = self.file + copysign(i, file - self.file)
                if Board.free(scanner.rank, scanner.file) is not None:
                    return False
        return Piece.canmove(self, rank, file)

class Rook(Piece):

    def canmove(self, rank, file):
        if (self.rank == rank) + (self.file == file) != 1:
            return False
        else:
            scanner = Scanner(self.rank, self.file)
            squares = max(abs(rank - self.rank), abs(file - self.file))
            for i in range(1, squares):
                scanner.rank = self.rank + i * (rank - self.rank) / squares
                scanner.file = self.file + i * (rank - self.rank) / squares
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
            if piece.canmove(self.rank, self.file):
                print("Check.", piece, piece.rank, piece.file)
                return True
        return False
        
    def canmove(self, rank, file):
        if rank - self.rank in [-1, 0, 1] and file - self.file in [-1, 0, 1] and rank - self.rank + file - self.file != 0:
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
                return Board.free(rank, file) == None
            if rank == 3 and file - self.file == 0 and self.rank == 1:
                    return Board.free(rank, file) == None and Board.free(rank - 1, file) == None
            if rank - self.rank == 1 and abs(file - self.file) == 1:
                if Board.free(rank, file) == None:
                    if Board.enpassant(rank - 1, file):
                        return True
                    return False
                else:
                    return Piece.canmove(self, rank, file)
            return False
        if self.colour == "B":
            if rank - self.rank == -1 and file - self.file == 0:
                return Board.free(rank, file) == None
            if rank == 4 and file - self.file == 0 and self.rank == 6:
                    return Board.free(rank, file) == None and Board.free(rank + 1, file) == None
            if rank - self.rank == -1 and abs(file - self.file) == 1:
                if Board.free(rank, file) == None:
                    if Board.enpassant(rank + 1, file):
                        return True
                    return False
                else:
                    return Piece.canmove(self, rank, file)
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
whiteB = [b1, b2]
whiteR = [r1, r2]
whiteQ = [q1]
whiteN = [n1, n2]
whiteP = [p1, p2, p3, p4, p5, p6, p7, p8]
blackB = [b3, b4]
blackR = [r3, r4]
blackQ = [q2]
blackN = [n3, n4]
blackP = [p9, p10, p11, p12, p13, p14, p15, p16]

tomove = "W"

def display():
    sahovnica = []
    for i in range(8):
        row = []
        for j in range(8):
            if Board.free(i, j) is None:
                row.append(" ")
            else:
                if Board.free(i, j) in whiteP:
                    row.append("P")
                if Board.free(i, j) in whiteN:
                    row.append("N")
                if Board.free(i, j) in whiteB:
                    row.append("B")
                if Board.free(i, j) in whiteR:
                    row.append("R")
                if Board.free(i, j) in whiteQ:
                    row.append("Q")
                if Board.free(i, j) == k1:
                    row.append("K")
                if Board.free(i, j) in blackP:
                    row.append("p")
                if Board.free(i, j) in blackN:
                    row.append("n")
                if Board.free(i, j) in blackB:
                    row.append("b")
                if Board.free(i, j) in blackR:
                    row.append("r")
                if Board.free(i, j) in blackQ:
                    row.append("q")
                if Board.free(i, j) == k2:
                    row.append("k")
        sahovnica.append(row)
    return sahovnica

print("""\nInstructions:
When it is your turn to move, input the move you wish to make in algebraic notation.
If the input is invalid or the move you wish to make is illegal, you will be asked to input the move again.
\nAlgebraic notation:
To move a piece to a desired square, write the designated letter of the piece and the coordinates you wish to land on. For example:
Qh5 - Queen to h5
Nf3 - Knight to f3
Please note that the letter used to designate the piece must always be capitalised.
Also note that the pawn does not have a designated letter:
e4 - pawn to e4
If you wish to take a piece, write the letter x between the piece and the square, thus:
Qxe5 - Queen takes e5
exd5 - the pawn on the e file takes d5.
If the move you make is a check, you don't have to write the '+' sign at the end of your input.
However, if you wish to promote a pawn, you will need to input the piece you wish to promote to:
e8=Q - pawn to e8, promotes to a queen.
The input: 'e8' will be considered invalid notation.
\n""")

while True:
    if tomove == "W":
        position = {piece: (piece.rank, piece.file) for piece in pieces}.copy()
        illegal = False
        for i in display()[::-1]:
            print(i)
        move = input("White to move: ")
        if len(move) == 2:
            if move[0] not in "abcdefgh" or move[1] not in "1234567":
                illegal = True
            else:
                rank = int(move[1]) - 1
                file = ord(move[0]) - 97
                illegal = all(not pawn.canmove(rank, file) for pawn in whiteP)
                for pawn in whiteP:
                    pawn.move(rank, file)
        if len(move) == 3:
            if move[0] not in "BQNKR" or move[1] not in "abcdefgh" or move[2] not in "12345678":
                print("Invalid notation.")
                illegal = True
            else:
                piece = move[0]
                rank = int(move[2]) - 1
                file = ord(move[1]) - 97
                if piece == "K":
                    k1.move(rank, file)
                if piece == "Q":
                    illegal = all(not queen.canmove(rank, file) for queen in whiteQ)
                    for queen in whiteQ:
                        queen.move(rank, file)
                if piece == "B":
                    illegal = all(not bishop.canmove(rank, file) for bishop in whiteB)
                    for bishop in whiteB:
                        bishop.move(rank, file)
                if piece == "N":
                    illegal = all(not knight.canmove(rank, file) for knight in whiteN)
                    for knight in whiteN:
                        knight.move(rank, file)
                if piece == "R":
                    illegal = all(not rook.canmove(rank, file) for rook in whiteR)
                    for rook in whiteR:
                        rook.move(rank, file)
        if len(move) == 4:
            if move[0] in "abcdefgh" and move[1] == "8" and move[2] == "=" and move[3]:
                file = ord(move[0]) - 97
                illegal = all(not pawn.canmove(7, file) for pawn in whiteP)
                for pawn in whiteP:
                    if pawn.canmove(7, file):
                        if move[3] == "R":
                            pawn.move(7, file)
                            whiteP.remove(pawn)
                            whiteR.append(pawn)
                        elif move[3] == "N":
                            pawn.move(7, file)
                            whiteP.remove(pawn)
                            whiteN.append(pawn)
                        elif move[3] == "B":
                            pawn.move(7, file)
                            whiteP.remove(pawn)
                            whiteB.append(pawn)
                        elif move[3] == "Q":
                            pawn.move(7, file)
                            whiteP.remove(pawn)
                            whiteQ.append(pawn)
                        else:
                            print("Invalid notation.")
                            illegal = True
            else:
                print("Invalid notation.")
                illegal = True
        tomove = "B"
        if k1.check():
            illegal = True
        if illegal:
            print("Illegal move.")
            for piece, coords in position.items():
                piece.rank = coords[0]
                piece.file = coords[1]
            tomove = "W"

    if tomove == "B":
        position = {piece: (piece.rank, piece.file) for piece in pieces}.copy()
        illegal = False
        for i in display():
            print(i)
        move = input("Black to move: ")
        if len(move) == 2:
            rank = int(move[1]) - 1
            file = ord(move[0]) - 97
            illegal = all(not pawn.canmove(rank, file) for pawn in blackP)
            for pawn in blackP:
                pawn.move(rank, file)
        if len(move) == 3:
            piece = move[0]
            rank = int(move[2]) - 1
            file = ord(move[1]) - 97
            if piece == "K":
                k2.move(rank, file)
            if piece == "Q":
                illegal = all(not queen.canmove(rank, file) for queen in blackQ)
                for queen in blackQ:
                    queen.move(rank, file)
            if piece == "B":
                illegal = all(not bishop.canmove(rank, file) for bishop in blackB)
                for bishop in blackB:
                    bishop.move(rank, file)
            if piece == "N":
                illegal = all(not knight.canmove(rank, file) for knight in blackN)
                for knight in blackN:
                    knight.move(rank, file)
            if piece == "R":
                illegal = all(not rook.canmove(rank, file) for rook in blackR)
                for rook in blackR:
                    rook.move(rank, file)
        tomove = "W"
        if k2.check():
            illegal = True
        if illegal:
            print("Illegal move.")
            for piece, coords in position.items():
                piece.rank = coords[0]
                piece.file = coords[1]
            tomove = "B"