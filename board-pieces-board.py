def board_to_pieces(board):
    pieces = []
    for i in board:
        for j in i:
            if j != " ":
                piece = [King, Pawn, Knight, Bishop, Rook, Queen][j in "Pp" + \
                2 * j in "Nn" + 3 * j in "Bb" + 4 * j in "Rr" + 5 * j in "Qq"]
                pieces.append(piece(i, j, j.isupper()))
    return pieces

def pieces_to_board(pieces):
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