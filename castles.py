rooks = [[r3, r4], [r1, r2]]
kings = [k2, k1]
pieces = [k1, k2, r1, r2, r3, r4]

#colour: Bool
#side: Bool -> True = kingside, False = queenside
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