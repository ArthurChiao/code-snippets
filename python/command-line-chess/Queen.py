from Piece import Piece
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class Queen(Piece):

    stringRep = 'Q'
    value = 9

    def __init__(self, board, side, position, movesMade=0):
        super(Queen, self).__init__(board, side, position)
        self.movesMade = movesMade

    def get_possible_moves(self):
        pos = self.position # current position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0), C(1, 1),
                      C(1, -1), C(-1, 1), C(-1, -1)]
        for d in directions:
            for move in self.move_in_direction(pos, d, self.side):
                yield move
