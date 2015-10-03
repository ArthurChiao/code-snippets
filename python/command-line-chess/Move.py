class Move:

    def __init__(self, piece, new_pos, piece_to_capture=None):
        self.notation = None
        self.check = False
        self.checkmate = False
        self.kingsideCastle = False
        self.queensideCastle = False
        self.promotion = False
        self.pessant = False
        self.stalemate = False

        self.piece = piece
        self.old_pos = piece.position
        self.new_pos = new_pos
        self.piece_to_capture = piece_to_capture
        # For en pessant and castling
        self.specialMovePiece = None
        # For castling
        self.rookMove = None

    def __str__(self):
        displayString = 'Old pos : ' + str(self.old_pos) + \
                        ' -- New pos : ' + str(self.new_pos)
        if self.notation:
            displayString += ' Notation : ' + self.notation
        if self.pessant:
            displayString = 'Old pos : ' + str(self.old_pos) + \
                            ' -- New pos : ' + str(self.new_pos) + \
                            ' -- Pawn taken : ' + str(self.specialMovePiece)
            displayString += ' PESSANT'
        return displayString

    def __eq__(self, other):
        if self.old_pos == other.old_pos and \
           self.new_pos == other.new_pos and \
           self.specialMovePiece == other.specialMovePiece:
            if not self.specialMovePiece:
                return True
            if self.specialMovePiece and \
               self.specialMovePiece == other.specialMovePiece:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash((self.old_pos, self.new_pos))

    def reverse(self):
        return Move(self.piece, self.piece.position,
                    piece_to_capture=self.piece_to_capture)
