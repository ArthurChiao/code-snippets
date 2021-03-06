from Piece import Piece
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class Rook (Piece):

    stringRep = 'R'
    value = 5

    def __init__(self, board, side, position,  movesMade=0):
        super(Rook, self).__init__(board, side, position)
        self.movesMade = movesMade

    def get_possible_moves(self):
        '''
        Get all possible moves starting from current position

        @return a Move list
        '''
        pos = self.position # current position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0)]
        for d in directions:
            for move in self.move_in_direction(pos, d, self.side):
                yield move
