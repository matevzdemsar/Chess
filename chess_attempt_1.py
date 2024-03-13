white = ["P","P","P","P","P","P","P","P", "R", "R", "N", "N", "B", "B", "Q", "K"]
black = ["p", "p", "p", "p", "p", "p", "p", "p", "r", "r", "n", "n", "b", "b", "q", "k"]
sahovnica = [["R", "N", "B", "Q", "K", "B", "N", "R"],
             ["P", "P", "P", "P", "P", "P", "P", "P"],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             ["p", "p", "p", "p", "p", "p", "p", "p"],
             ["r", "n", "b", "q", "k", "b", "n", "r"]]
tm = 0
print("""Instructions:
    The moves are to be entered by writing down which square the piece is moving from, followed by the square to which it moves.
    For example, moving the pawn from a2 to a4 should look like this:
    White to move: a2a4.
    Only lowercase letters are to be used.
    If you are checkmated or wish to resign, enter the symbol #.
    """)


def canmove(rank1, file1, polje):
    figura = sahovnica[rank1][file1]
    polja = []
    if tm == 0 and (figura not in white or sahovnica[polje[0]][polje[1]] in white):
        print(1)
        return False
    if tm == 1 and (figura not in black or sahovnica[polje[0]][polje[1]] in black):
        print(2)
        return False
    if rank1 not in range(8) or file1 not in range(8) or rank2 not in range(8) or file2 not in range(8):
        print(3)
        return False
    if [rank1, file1] == [rank2, file2]:
        print(4)
        return False
    if not unobstructed(rank1, file1, polje):
        print("Obstructed.")
        return False
    if figura == "P":
        if sahovnica[rank1 + 1][file1] not in white and sahovnica[rank1 + 1][file1] not in black:
            polja.append([rank1 + 1, file1])
        if figura in sahovnica[1]:
            if sahovnica[3][file1] not in white and sahovnica[3][file1] not in black and [rank1 + 1, file1] in polja:
                polja.append([rank1 + 2, file1])
        if file1 + 1 in range(8) and sahovnica[rank1 + 1][file1 + 1] in black:
            polja.append([rank1 + 1, file1 + 1])
        if file1 - 1 in range(8) and sahovnica[rank1 + 1][file1 - 1] in black:
            polja.append([rank1 + 1, file1 - 1])
        #if sahovnica[rank1 + 1][file1 + 1] not in white and sahovnica[rank1 + 1][file1 + 1] not in black and en_passant_w == 1:
            #polja.append(sahovnica[rank1 + 1][file1 + 1])
        #if sahovnica[rank1 + 1][file1 - 1] not in white and sahovnica[rank1 + 1][file1 - 1] not in black and en_passant_w == 1:
            #polja.append(sahovnica[rank1 + 1][file1 - 1])
        if polje in polja:
            return True
        else:
            return False
    if figura == "p":
        if sahovnica[rank1 - 1][file1] not in white and sahovnica[rank1 - 1][file1] not in black:
            polja.append([rank1 - 1, file1])
        if figura in sahovnica[6]:
            if sahovnica[4][file1] not in white and sahovnica[4][file1] not in black and [rank1 - 1, file1] in polja:
                polja.append([rank1 - 2, file1])
        if file1 + 1 in range(8) and sahovnica[rank1 - 1][file1 + 1] in white:
            polja.append([rank1 - 1, file1 + 1])
        if file1 - 1 in range(8) and sahovnica[rank1 - 1][file1 - 1] in white:
            polja.append([rank1 - 1, file1 - 1])
        #if sahovnica[rank1 - 1][file1 + 1] not in white and sahovnica[rank1 - 1][file1 + 1] not in black and en_passant_b == 1:
            #polja.append(sahovnica[rank1 - 1][file1 + 1])
        #if sahovnica[rank1 - 1][file1 - 1] not in white and sahovnica[rank1 - 1][file1 - 1] not in black and en_passant_b == 1:
            #polja.append(sahovnica[rank1 - 1][file1 - 1])
        if [rank2, file2] in polja:
            return True
        else:
            return False
    if figura == "R" or figura == "r":
        if rank1 == rank2 or file1 == file2:
            return True
        else: return False
    if figura == "B" or figura == "b":
        if file1 + rank1 == file2 + rank2 or file1 - rank1 == file2 - rank2:
            return True
        else: return False
    if figura == "Q" or figura == "q":
        if rank1 == rank2 or file1 == file2 or file1 + rank1 == file2 + rank2 or file1 - rank1 == file2 - rank2:
            return True
        else: return False
    if figura == "K" or figura == "k":
        if (rank1 - rank2 in [-1, 0, 1]) and (file1 - file2 in [-1, 0, 1]) and rank2 in range(8) and file2 in range(8):
            return True
        else: return False
    if figura == "N" or figura == "n":
            if rank2 in range(8) and file2 in range(8) and abs((file1 - file2) * (rank1 - rank2)) == 2:
                return True
            else: return False
# Add en passant


def findwhiteking():
    for i in range(8):
        if "K" in sahovnica[i]:
            return [i, sahovnica[i].index("K")]
        

def findblackking():
    for i in range(8):
        if "k" in sahovnica[i]:
            return [i, sahovnica[i].index("k")]


def whiteknights():
    squares = []
    for i in range(8):
        for j in range(8):
            if sahovnica[i][j] == "N":
                squares.append([i, j])
    return squares


def blackknights():
    squares = []
    for i in range(8):
        for j in range(8):
            if sahovnica[i][j] == "n":
                squares.append([i, j])
    return squares


def whitebishop(scanner):
    scan = sahovnica[scanner[0]][scanner[1]]
    if scan == "B" or scan == "Q":
        return True
    elif (scan in white or scan in black) and scan != "k":
        return False
    else: return None


def whiterook(scanner):
    scan = sahovnica[scanner[0]][scanner[1]]
    if scan == "R" or scan == "Q":
        return True
    elif (scan in white or scan in black) and scan != "k":
        return False
    else: return None


def blackbishop(scanner):
    scan = sahovnica[scanner[0]][scanner[1]]
    if scan == "b" or scan == "q": return True
    elif (scan in white or scan in black) and scan != "K":
        return False
    else: return None


def blackrook(scanner):
    scan = sahovnica[scanner[0]][scanner[1]]
    if scan == "r" or scan == "q": return True
    elif (scan in white or scan in black) and scan != "K":
        return False
    else: return None


def whiteincheck():
    rank = findwhiteking()[0]
    file = findwhiteking()[1]
    for i in blackknights():
        if abs((i[0] - rank) * (i[1] - file)) == 2:
            return True
    if sahovnica[rank + 1][file + 1] == "p" or sahovnica[rank + 1][file - 1] == "p":
        return True
    scanner = [rank, file]
    for i in range(file + 1):
        scanner = [rank, file - i]
        if blackrook(scanner) is True:
            return True
        elif blackrook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(8 - file):
        scanner = [rank, file + i]
        if blackrook(scanner) is True:
            return True
        elif blackrook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(rank + 1):
        scanner = [rank - i, file]
        if blackrook(scanner) is True:
            return True
        elif blackrook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(8 - rank):
        scanner = [rank + i, file]
        if blackrook(scanner) is True:
            return True
        elif blackrook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(rank + 1, file + 1)):
        scanner = [rank - i, file - i]
        if blackbishop(scanner) is True:
            return True
        elif blackbishop(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(rank + 1, 8 - file)):
        scanner = [rank - i, file + i]
        if blackbishop(scanner) is True:
            return True
        elif blackbishop(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(8 - rank, file + 1)):
        scanner = [rank + i, file - i]
        if blackbishop(scanner) is True:
            return True
        elif blackbishop(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(8 - rank, 8 - file)):
        scanner = [rank + i, file + i]
        if blackbishop(scanner) is True:
            return True
        elif blackbishop(scanner) is False:
            break
    return False


def blackincheck():
    rank = findblackking()[0]
    file = findwhiteking()[1]
    for i in blackknights():
        if abs((i[0] - rank) * (i[1] - file)) == 2:
            return True
    if sahovnica[rank - 1][file + 1] == "P" or sahovnica[rank - 1][file - 1] == "P":
        return True
    scanner = [rank, file]
    for i in range(file + 1):
        scanner = [rank, file - i]
        if whiterook(scanner) is True:
            return True
        elif whiterook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(8 - file):
        scanner = [rank, file + i]
        if whiterook(scanner) is True:
            return True
        elif whiterook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(rank + 1):
        scanner = [rank - i, file]
        if whiterook(scanner) is True:
            return True
        elif whiterook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(8 - rank):
        scanner = [rank + i, file]
        if whiterook(scanner) is True:
            return True
        elif whiterook(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(rank + 1, file + 1)):
        scanner = [rank - i, file - i]
        if whitebishop(scanner) is True:
            return True
        elif whitebishop(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(rank + 1, 8 - file)):
        scanner = [rank - i, file + i]
        if whitebishop(scanner) is True:
            return True
        elif whitebishop(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(8 - rank, file + 1)):
        scanner = [rank + i, file - i]
        if whitebishop(scanner) is True:
            return True
        elif whitebishop(scanner) is False:
            break
    scanner = [rank, file]
    for i in range(min(8 - rank, 8 - file)):
        scanner = [rank + i, file + i]
        if whitebishop(scanner) is True:
            return True
        elif whitebishop(scanner) is False:
            break
    return False


def unobstructed(rank1, file1, polje):
    figura = [rank1, file1]
    scanner = [rank1, file1]
    if figura == " ":
        return False
    elif figura == "R" or figura == "r":
        if rank1 == rank2 and file1 > file2:
            for i in range(file1 - file2):
                scanner = [rank1, file1 - i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False           
        if rank1 == rank2 and file1 < file2:
            for i in range(file2 - file1):
                scanner = [rank1, file1 + i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 == file2 and rank1 > rank2:
            for i in range(rank1 - rank2):
                scanner = [rank1 - i, file1]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 == file2 and rank1 < rank2:
            for i in range(rank2 - rank1):
                scanner = [rank1 + i, file1]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
    elif figura == "B" or figura == "b":
        if rank1 > rank2 and file1 > file2:
            for i in range(file1 - file2):
                scanner = [rank1 - i, file1 - i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False                
        if rank1 > rank2 and file1 < file2:
            for i in range(file2 - file1):
                scanner = [rank1 - i, file1 + i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 > file2 and rank1 < rank2:
            print("c")
            for i in range(rank1 - rank2):
                scanner = [rank1 + i, file1 - i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 < file2 and rank1 < rank2:
            for i in range(rank2 - rank1):
                scanner = [rank1 + i, file1 + i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
    elif figura == "Q" or figura == "q":
        if rank1 == rank2 and file1 > file2:
            for i in range(file1 - file2):
                scanner = [rank1, file1 - i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False                
        if rank1 == rank2 and file1 < file2:
            for i in range(file2 - file1):
                scanner = [rank1, file1 + i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 == file2 and rank1 > rank2:
            for i in range(rank1 - rank2):
                scanner = [rank1 - i, file1]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 == file2 and rank1 < rank2:
            for i in range(rank2 - rank1):
                scanner = [rank1 + i, file1]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if rank1 > rank2 and file1 > file2:
            for i in range(file1 - file2):
                scanner = [rank1 - i, file1 - i]
                if scanner != polje and scanner != figura and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False                
        if rank1 > rank2 and file1 < file2:
            for i in range(file2 - file1):
                print(scanner)
                scanner = [rank1 - i, file1 + i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 > file2 and rank1 < rank2:
            for i in range(rank1 - rank2):
                scanner = [rank1 + i + 1, file1 - i - 1]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
        if file1 < file2 and rank1 < rank2:
            for i in range(rank2 - rank1):
                scanner = [rank1 + i, file1 + i]
                if scanner != polje and scanner != figura and sahovnica[scanner[0]][scanner[1]] in white or sahovnica[scanner[0]][scanner[1]] in black:
                    return False
    else: return True

def movepiece(whiteking, blackking, tm):
    legal = canmove(rank1, file1, polje)
    tmp = tm
    tmpw = whiteking
    tmpb = blackking
    tmppolje = sahovnica[polje[0]][polje[1]]
    if legal == True:
        sahovnica[rank2][file2] = sahovnica[rank1][file1]
        sahovnica[rank1][file1] = " "
        if tmp == 0 and whiteincheck() == True:
            sahovnica[rank1][file1] = sahovnica[rank2][file2]
            sahovnica[rank2][file2] = tmppolje
            whiteking = tmpw
            print("Illegal move, you are in check.")
            tmp = 0
            return sahovnica, tmp
        elif tmp == 0:
            if "P" in sahovnica[7]:
                while True:
                    newpiece = str(input("Which piece would you like to promote to? (N, B, R, Q): "))
                    if newpiece in "NBRQ":
                        sahovnica[7][sahovnica[7].index("P")] = newpiece
                        break
            tmp = 1
            return sahovnica, tmp
        if tmp == 1 and blackincheck():
            sahovnica[rank1][file1] = sahovnica[rank2][file2]
            sahovnica[rank2][file2] = tmppolje
            blackking = tmpb
            print("Illegal move, you are in check.")
            tmp = 1
            return sahovnica, tmp
        elif tmp == 1:
            if "p" in sahovnica[0]:
                while True:
                    newpiece = str(input("Which piece would you like to promote to? (n, b, r, q): "))
                    if newpiece in "nbrq":
                        sahovnica[1][sahovnica[1].index("p")] = newpiece
            tmp = 0
            return sahovnica, tmp

while True:
    if tm == 0:
        whiteking = findwhiteking()
        blackking = findblackking()
        #en_passant_b = 0
        beliPOV = reversed(sahovnica)
        for i in beliPOV:
            print(i)
        move = input("White to move: ")
        if move == "#":
            print("Black wins!")
            break
        if len(move) != 4 or move[0] not in "abcdefgh" or move[1] not in "12345678" or move[2] not in "abcdefgh" or move[3] not in "12345678":
            print("Invalid input.")
            tm = 2
            tm = 0
        else:
            rank1 = int(move[1]) - 1
            file1 = ord(move[0]) - 97
            rank2 = int(move[3]) - 1
            file2 = ord(move[2]) - 97
            polje = [rank2, file2]
            legal = canmove(rank1, file1, polje)
            if legal == False:
                print("Illegal move, it's because of canmove.")
                tm = 2
                tm = 0
            if legal == True:
                sahovnica, tm = movepiece(whiteking, blackking, tm)
    if tm == 1:
        #en_passant_w = 0
        for i in sahovnica:
            print(i)
        move = input("Black to move: ")
        if move == "#":
            print("White wins!")
            break
        if len(move) != 4 or move[0] not in "abcdefgh" or move[1] not in "12345678" or move[2] not in "abcdefgh" or move[3] not in "12345678":
            print("Invalid input.")
            tm = 2
            tm = 1
        else:
            rank1 = int(move[1]) - 1
            file1 = ord(move[0]) - 97
            rank2 = int(move[3]) - 1
            file2 = ord(move[2]) - 97
            polje = [rank2, file2]
            figura = sahovnica[rank1][file1]
            legal = canmove(rank1, file1, polje)
            if legal == False:
                print("Illegal move, it's becuase of canmove.")
                tm = 2
                tm = 1
            if legal == True:
                sahovnica, tm = movepiece(whiteking, blackking, tm)
