from math import copysign

class Piece:

    def __init__(self, rank, file, colour, has_moved=False):
        self.rank = rank
        self.file = file
        self.colour = colour
        self.has_moved = has_moved

    def can_move(self, rank, file):
        target = Board.occ(rank, file)
        if not target:
            return True
        else:
            return target.colour != self.colour
    
    def move(self, rank, file):
        self.rank = rank
        self.file = file


class Knight(Piece):
    
    def can_move(self, rank, file, en_passant=False):
        if abs((rank - self.rank) * (file - self.file)) != 2:
            return False
        else:
            return Piece.can_move(self, rank, file)


class Bishop(Piece):
    
    def can_move(self, rank, file, en_passant=False):
        if abs(rank - self.rank) != abs(file - self.file):
            return False
        else:
            for i in range(1, abs(rank - self.rank)):
                square = Board.occ(self.rank + copysign(i, rank - self.rank), self.file + copysign(i, file - self.file))
                if square:
                    return False
            return Piece.can_move(self, rank, file)


class Rook(Piece):
    
    def can_move(self, rank, file, en_passant=False):
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
    
    def can_move(self, rank, file, en_passant=False):
        if abs(rank - self.rank) != abs(file - self.file) and \
        (self.rank == rank) + (self.file == file) != 1:
            return False
        else:
            dist = max(abs(self.file - file), abs(self.rank - rank))
            for i in range(1, dist):
                square = Board.occ(self.rank + i * (rank - self.rank) / dist, self.file + i * (file - self.file) / dist)
                if square:
                    return False
            return Piece.can_move(self, rank, file)


class King(Piece):

    def can_move(self, rank, file, en_passant=False):
        dy = abs(rank - self.rank)
        dx = abs(file - self.file)
        if dx in (0, 1) and dy in (0, 1) and dx + dy != 2:
            return Piece.can_move(self, rank, file)
        return False


class Pawn(Piece):

    def can_move(self, rank, file, en_passant=False):
        if self.file == file:
            if rank == self.rank + 2 * tomove - 1 and self.colour == tomove:
                return Piece.can_move(self, rank, file)
            elif rank == self.rank + 4 * tomove - 2:
                if Board.occ(rank, file) or Board.occ(rank - 2 * tomove + 1, file) and \
                self.rank not in (1, 6) and self.colour == tomove:
                    return False
                else:
                    return True
        elif abs(self.file - file) == 1 and rank == self.rank + 2 * tomove - 1:
            target = Board.occ(rank, file)
            if target is not False:
                return target.colour != self.colour
            else:
                return (rank, file, not self.colour) == en_passant
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


class Any():
    
    def __eq__(self, other):
        return True


def board_to_pieces(board):
    pieces = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            square = board[i][j]
            if board[i][j] != " ":
                piece = [King, Pawn, Knight, Bishop, Rook, Queen][(square in "Pp") + \
                2 * (square in "Nn") + 3 * (square in "Bb") + 4 * (square in "Rr") + 5 * (square in "Qq")]
                pieces.append(piece(i, j, square.isupper()))
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
                symb = "kpnrqb"[(t is Pawn) + 2 * (t is Knight) + 3 * (t is Rook) + 4 * (t is Queen) + 5 * (t is Bishop)]
                if piece.colour:
                    row.append(symb.upper())
                else:
                    row.append(symb)
        board.append(row)
    return board


def fen_decrypt(string):
    board = []
    string = string.split(" ")
    rows = string[0].split("/")
    for i in rows:
        row = []
        for j in i:
            if not j.isdigit():
                row.append(j)
            else:
                for x in range(int(j)):
                    row.append(" ")
        board.append(row)
        ep = (int(string[3][1]) - 1, ord(string[3][1]) - 97)
    return board, string[1] == "w", string[2], ep, int(string[4]), int(string[5])


def fen_encrypt(board, tomove, castle, en_passant, hmove, fmove):
    string = ""
    for i in range(len(board)):
        empty = 0
        for j in board[i]:
            if j == " ":
                empty += 1
            else:
                if empty:
                    string += str(empty)
                    empty = 0
                string += j
        if empty:
            string += str(empty)
            empty = 0
        if i < 7:
            string += "/"
    string += f" {'w' * tomove}{'b' * (1 - tomove)}" + " " + castle + " "
    return string + " " + en_passant + " " + str(hmove) + " " + str(fmove)


def castle_str():
    castle_w = f"{'K' * (not r2.has_moved) + 'Q' * (not r1.has_moved)}"
    castle_b = f"{'k' * (not r4.has_moved) + 'q' * (not r3.has_moved)}"
    castle = f"{castle_w * (not k1.has_moved) + castle_b * (not k2.has_moved)}"
    if not len(castle):
        castle = "-"
    return castle
        
def display(board, tomove):
    if tomove:
        for i in board[::-1]:
            print(i)
    else:
        for i in board:
            print(i[::-1])


def is_legal(tomove, exception=None):
    king = kings[tomove]
    for piece in pieces:
        if piece.can_move(king.rank, king.file) and piece != exception:
            return False
    return True


def castles(colour, side):
    king = kings[colour]
    rook = rooks[colour][side]

    if king.has_moved or rook.has_moved:
        return False
    elif not rook.can_move(king.rank, king.file - 2 * side + 1):
        return False
    elif not is_legal(tomove):
        return False
    else:
        king.file -= 2 * side - 1
        if not is_legal(colour):
            king.file += 2 * side - 1
            return False
        king.file -= 2 * side - 1
        if not is_legal(colour):
            king.file += 4 * side - 2
            return False
        rook.move(king.rank, king.file + 2 * side - 1)
        king.has_moved = True
        rook.has_moved = True
        return True


def get_move(tomove):

    move = input(f"{'White' * tomove}{'Black' * (1 - tomove)} to move: ")

    if len(move) - 1:
        move = move.replace("+", "").replace("#", "")
    
    if move == "#":
        return None
    
    if len(move) == 2:
        if move[0] in "abcdefgh" and move[1] in "234567":
            return (Pawn, Any(), Any()), int(move[1]) - 1, ord(move[0]) - 97, Pawn
        return False
    
    if len(move) == 3:
        if move == "0-0":
            return "kingside"
        if move[0] in "BQNKR" and move[1] in "abcdefgh" and move[2] in "12345678":
            piece = [Bishop, Queen, Knight, Rook, King][(move[0] == "Q") + \
            2 * (move[0] == "N") + 3 * (move[0] == "R") + 4 * (move[0] == "K")]
            return (piece, Any(), Any()), int(move[2]) - 1, ord(move[1]) - 97, piece
        return False
    
    if len(move) == 4:
        if move[0] in "BQNKR" and move[1] == "x" and move[2] in "abcdefgh" and move[3] in "12345678":
            piece = [Bishop, Queen, Knight, Rook, King][(move[0] == "Q") + \
            2 * (move[0] == "N") + 3 * (move[0] == "R") + 4 * (move[0] == "K")]
            return (piece, Any(), Any()), int(move[3]) - 1, ord(move[2]) - 97, piece
        if move[0] in "abcdefgh" and move[1] == "x" and move[2] in "abcdefgh" and move[3] in "234567":
            return (Pawn, Any(), ord(move[0]) - 97), int(move[3]) - 1, ord(move[2]) - 97, Pawn
        if move[0] in "abcdefgh" and move[1] in "18" and move[2] == "=" and move[3] in "BRQN":
            piece = [Bishop, Rook, Queen, Knight][(move[3] == "R") + 2 * (move[3] == "Q") + 3 * (move[3] == "N")]
            return (Pawn, Any(), Any()), int(move[1]) - 1, ord(move[0]) - 97, piece
        if move[0] in "BRQN" and move[1] in "abcdefgh" and move[2] in "abcdefgh" and move[3] in "12345678":
            piece = [Bishop, Rook, Queen, Knight][(move[0] == "R") + 2 * (move[0] == "Q") + 3 * (move[0] == "N")]
            return (piece, Any(), ord(move[1]) - 97), int(move[3]) - 1, ord(move[2]) - 97,  piece
        if move[0] in "BRQN" and move[1] in "12345678" and move[2] in "abcdefgh" and move[3] in "12345678":
            piece = [Bishop, Rook, Queen, Knight][(move[0] == "R") + 2 * (move[0] == "Q") + 3 * (move[0] == "N")]
            return (piece, int(move[1]) - 1, Any()), int(move[3]) - 1, ord(move[2]) - 97, piece
        return False
    
    if len(move) == 5:
        if move == "0-0-0":
            return "queenside"
        if move[0] in "BRQN" and move[1] in "abcdefgh" and move[2] == "x" \
            and move[3] in "abcdefgh" and move[4] in "12345678":
            piece = [Bishop, Rook, Queen, Knight][(move[0] == "R") + 2 * (move[0] == "Q") + 3 * (move[0] == "N")]
            return (piece, Any(), ord(move[1]) - 97), int(move[4]) - 1, ord(move[3]) - 97, piece
        if move[0] in "BRQN" and move[1] in "12345678" and move[2] == "x" \
            and move[3] in "abcdefgh" and move[4] in "12345678":
            piece = [Bishop, Rook, Queen, Knight][(move[0] == "R") + 2 * (move[0] == "Q") + 3 * (move[0] == "N")]
            return (piece, int(move[1]) - 1, Any()), int(move[4]) - 1, ord(move[3]) - 97, piece
        if move[0] in "BRQN" and move[1] in "abcdefgh" and move[2] in "12345678" \
            and move[3] in "abcdefgh" and move[4] in "12345678":
            piece = [Bishop, Rook, Queen, Knight][(move[0] == "R" )+ 2 * (move[0] == "Q") + 3 * (move[0] == "N")]
            return (piece, int(move[2]) - 1, ord(move[1]) - 97), int(move[4]) - 1, ord(move[3]) - 97, piece
        return False
    
    if len(move) == 6:
        if move[0] in "abcdefgh" and move[1] == "x" and move[2] in "abcdefgh" \
            and move[3] in "18" and move[4] == "=" and move[5] in "BRQN":
            piece = [Bishop, Rook, Queen, Knight][(move[5] == "R") + 2 * (move[5] == "Q") + 3 * (move[5] == "N")]
            return (Pawn, Any(), Any()), int(move[3]) - 1, ord(move[2]) - 97, piece
        if move[0] in "BRQN" and move[1] in "abcdefgh" and move[2] in "12345678" \
            and move[3] == "x" and move[4] in "abcdefgh" and move[5] in "12345678":
            piece = [Bishop, Rook, Queen, Knight][(move[0] == "R" )+ 2 * (move[0] == "Q") + 3 * (move[0] == "N")]
            return (piece, int(move[2]) - 1, ord(move[1]) - 97), int(move[5]) - 1, ord(move[4]) - 97, piece
        return False
    
    return False


def legal_move(piece, rank, file):
    lm = []
    piece_type = [x for x in pieces if (type(x) == piece[0]) \
    and (x.rank == piece[1]) and (x.file == piece[2]) and x.colour == tomove]
    for i in piece_type:
        if i.can_move(rank, file, en_passant):
            coords = i.rank, i.file
            i.move(rank, file)                                      # i.rank, i.file = rank, file
            target = Board.occ(rank, file)
            if is_legal(i.colour, target):
                lm.append(i)
            i.rank, i.file = coords
    return lm[0] if len(lm) == 1 else False


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

pieces = [b1, b2, b3, b4, r1, r2, r3, r4, q1, q2, k1, k2, p1, p2, p3, \
p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, n1, n2, n3, n4]
kings = [k2, k1]
rooks = [[r4, r3], [r2, r1]]
tomove = True
en_passant = False
hmove = 0
fmove = 0
posits = {}

while True:
    legal = True
    board = pieces_to_board()
    display(board, tomove)
    move = get_move(tomove)
    if move is None:
        print(f"{'White' * (1 - tomove) + 'Black' * tomove} wins by resignation.")
        break
    if move is False:
        print("Invalid notation.")
        legal = False
    elif type(move) is tuple:
        piece_type, rank, file, becomes = move
        piece = legal_move(piece_type, rank, file)
        if not piece:
            legal = False
        else:
            target = Board.occ(rank, file)
            if target:
                Board.take(rank, file)
                hmove = 0
            elif en_passant == (rank, file, not tomove) and type(piece) is Pawn:
                Board.take(rank - 2 * tomove + 1, file)
            if type(piece) is Pawn:
                hmove = 0
                if becomes is not Pawn:
                    pieces[pieces.index(piece)] = becomes(rank, file, piece.colour)
                if abs(piece.rank - rank) == 2:
                    en_passant = (rank - 2 * tomove + 1, file, tomove)
            else:
                en_passant = False
            piece.move(rank, file)
            piece.has_moved = True
    else:
        legal = castles(tomove, move == "queenside")
            
    if legal:
        hmove += 1
        fmove += tomove
        tomove = not tomove

        if hmove == 101:
            print("Draw by 50-move rule.")
            break
        ep = f"{chr(en_passant[1]) + str(en_passant[0])}" if en_passant else "-"
        fen = fen_encrypt(board, tomove, castle_str(), ep, hmove, fmove)
        pos = fen.split(" ")[0]
        if pos not in posits:
            posits[pos] = 1
        else:
            posits[pos] += 1
            if posits[pos] == 3:
                print("Draw by threefold repetition.")
                break
    else:
        print("Illegal move.")