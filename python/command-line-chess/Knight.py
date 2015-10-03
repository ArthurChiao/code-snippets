from Piece import Piece
from Coordinate import Coordinate as C
from Move import Move

WHITE = True
BLACK = False


class Knight(Piece):

    stringRep = 'N'
    value = 3

    def __init__(self, board, side, position,  movesMade=0):
        super(Knight, self).__init__(board, side, position)
        self.movesMade = movesMade

    def get_possible_moves(self):
        board = self.board
        pos = self.position
        movements = [C(2, 1), C(2, -1), C(-2, 1), C(-2, -1), C(1, 2),
                     C(1, -2), C(-1, -2), C(-1, 2)]
        for movement in movements:
            new_pos = pos + movement
            if board.is_valid_pos(new_pos):
                piece_at_pos = board.get_piece_at_pos(new_pos)
                if piece_at_pos is None:
                    yield Move(self, new_pos)
                elif piece_at_pos.side != self.side:
                    yield Move(self, new_pos, piece_to_capture=piece_at_pos)
