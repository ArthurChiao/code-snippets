from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen

from Piece import Piece
from Coordinate import Coordinate as C
from Move import Move

WHITE = True
BLACK = False


class Pawn(Piece):

    stringRep = 'p'
    value = 1

    def __init__(self, board, side, position,  movesMade=0):
        super(Pawn, self).__init__(board, side, position)
        self.movesMade = movesMade

    # @profile
    def get_possible_moves(self):
        pos = self.position

        # Pawn moves one up
        movement = C(0, 1) if self.side == WHITE else C(0, -1)
        up_pos = pos + movement
        if self.board.is_valid_pos(up_pos):
            # Promotion moves
            if self.board.get_piece_at_pos(up_pos) is None:
                col = up_pos[1]
                if col == 7 or col == 0:
                    piecesForPromotion = \
                        [Rook(self.board, self.side, up_pos),
                         Knight(self.board, self.side, up_pos),
                         Bishop(self.board, self.side, up_pos),
                         Queen(self.board, self.side, up_pos)]
                    for piece in piecesForPromotion:
                        move = Move(self, up_pos)
                        move.promotion = True
                        move.specialMovePiece = piece
                        yield move
                else:
                    yield Move(self, up_pos)

        # Pawn moves two up
        if self.movesMade == 0:
            movement = C(0, 2) if self.side == WHITE else C(0, -2)
            up2_pos = pos + movement
            if self.board.is_valid_pos(up2_pos):
                if self.board.get_piece_at_pos(up2_pos) is None and \
                   self.board.get_piece_at_pos(up_pos) is None:
                    yield Move(self, up2_pos)

        # Pawn takes
        movements = [C(1, 1), C(-1, 1)] \
            if self.side == WHITE else [C(1, -1), C(-1, -1)]

        for movement in movements:
            new_pos = self.position + movement
            if self.board.is_valid_pos(new_pos):
                pieceToTake = self.board.get_piece_at_pos(new_pos)
                if pieceToTake and pieceToTake.side != self.side:
                    col = new_pos[1]
                    # Promotions
                    if col == 7 or col == 0:
                        piecesForPromotion = \
                            [Rook(self.board, self.side, new_pos),
                             Knight(self.board, self.side, new_pos),
                             Bishop(self.board, self.side, new_pos),
                             Queen(self.board, self.side, new_pos)]
                        for piece in piecesForPromotion:
                            move = Move(self, up_pos)
                            move.promotion = True
                            move.specialMovePiece = piece
                            yield move
                    else:
                        yield Move(self, new_pos,
                                   piece_to_capture=pieceToTake)

        # En pessant
        movements = [C(1, 1), C(-1, 1)] \
            if self.side == WHITE else [C(1, -1), C(-1, -1)]
        for movement in movements:
            posBesidePawn = self.position + C(movement[0], 0)
            if self.board.is_valid_pos(posBesidePawn):
                pieceBesidePawn = self.board.get_piece_at_pos(posBesidePawn)
                lastPieceMoved = self.board.getLastPieceMoved()
                lastMoveWasAdvanceTwo = False
                lastMove = self.board.getLastMove()

                if lastMove:
                    if lastMove.new_pos - lastMove.old_pos == C(0, 2) or \
                       lastMove.new_pos - lastMove.old_pos == C(0, -2):
                        lastMoveWasAdvanceTwo = True

                if pieceBesidePawn and \
                   pieceBesidePawn.stringRep == 'p' and \
                   pieceBesidePawn.side != self.side and \
                   lastPieceMoved is pieceBesidePawn and \
                   lastMoveWasAdvanceTwo:
                    move = Move(self, self.position + movement,
                                piece_to_capture=pieceBesidePawn)
                    move.pessant = True
                    move.specialMovePiece = pieceBesidePawn
                    yield move
