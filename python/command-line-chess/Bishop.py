from Piece import Piece
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class Bishop (Piece):

    stringRep = 'B'
    value = 3

    def __init__(self, board, side, position, movesMade=0):
        super(Bishop, self).__init__(board, side, position)
        self.movesMade = movesMade

    def get_possible_moves(self):
        pos = self.position
        directions = [C(1, 1), C(1, -1), C(-1, 1), C(-1, -1)]
        for d in directions:
            for move in self.move_in_direction(pos, d, self.side):
                yield move
