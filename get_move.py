
def get_move(tomove):
    valid = True
    if tomove:
        move = input("White to move: ")
    else:
        move = input("Black to move: ")
    move = move.replace("+", "").replace("#", "")
    
    if move == "#":
        return None
    
    if len(move) == 2:
        if move[0] in "abcdefgh" and move[1] in "234567":
            return "P", int(move[1]) - 1, ord(move[0]) - 97, False, "P"
        return False
    
    if len(move) == 3:
        if move == "0-0":
            return "kingside"
        if move[0] in "BQNKR" and move[1] in "abcdefgh" and move[2] in "12345678":
            return move[0], int(move[1]) - 1, ord(move[0]) - 97, False, move[0]
        return False
    
    if len(move) == 4:
        if move[0] in "BQNKR" and move[1] == "x" and move[2] in "abcdefgh" and move[3] in "12345678":
            return move[0], int(move[3]) - 1, ord(move[2]) - 97, True, move[0]
        if move[0] in "abcdefgh" and move[1] == "x" and move[2] in "abcdefgh" and move[3] in "234567":
            return "P", int(move[1]) - 1, ord(move[0]) - 97, True, "P"
        if move[0] in "abcdefgh" and move[1] in "18" and move[2] == "=" and move[3] in "BRQN":
            return "P", int(move[1]) - 1, ord(move[0]) - 97, False, move[3]
        if move[0] in "BRQN" and move[1] in "abcdefgh1234568" and move[2] in "abcdefgh" and move[3] in "12345678":
            return move[:2], int(move[3]) - 1, ord(move[2]) - 97, False, move[0]
        return False
    
    if len(move) == 5:
        if move == "0-0-0":
            return "queenside"
        if move[0] in "BRQN" and move[1] in "abcdefgh12345678" and move[2] == "x" and move[3] in "abcdefgh" and move[4] in "12345678":
            return move[:2], int(move[4]) - 1, ord(move[3]) - 97, True, move[0]
        if move[0] in "BRQN" and move[1] in "abcdefgh" and move[2] in "12345678" and move[3] in "abcdefgh" and move[4] in "12345678":
            return move[:3], int(move[4]) - 1, ord(move[3]) - 97, False, move[0]
        return False
    
    if len(move) == 6:
        if move[0] in "abcdefgh" and move[1] == "x" and move[2] in "abcdefgh" and move[3] in "18" and move[4] == "=" and move[5] in "BRQN":
            return "P", int(move[3]) - 1, ord(move[2]) - 97, True, move[5]
        if move[0] in "BRQN" and move[1] in "abcdefgh" and move[2] in "12345678" and move[3] == "x" and move[4] in "abcdefgh" and move[5] in "12345678":
            return move[:3], int(move[5]) - 1, ord(move[4]) - 97, True, move[0]
        return False
    
    return False

tomove = True
while True:
    move = get_move(tomove)
    if move is None:
        print(f"{'White' * (1 - tomove)}{'Black' * tomove} wins by resignation.")
        break
    elif move is False:
        print("Invalid notation")
    elif type(move) is tuple:
        piece, rank, file, take, become = move
        #canmove itd
    else:
        pass
        #castles
