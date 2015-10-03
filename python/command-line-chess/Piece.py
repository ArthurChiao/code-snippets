from Coordinate import Coordinate as C
from Move import Move

WHITE = True
BLACK = False
X = 0
Y = 1


class Piece:

    def __init__(self, board, side, position, movesMade=0):
        self.board = board
        self.side = side
        self.position = position
        self.movesMade = 0

    def __str__(self):
        sideString = 'White' if self.side == WHITE else 'Black'
        return 'Type : ' + type(self).__name__ + \
               ' - Position : ' + str(self.position) + \
               " - Side : " + sideString + \
               ' -- Value : ' + str(self.value) + \
               " -- Moves made : " + str(self.movesMade)

    def move_in_direction(self, pos, direction, side):
        '''
        Get next move in specified direction

        @param pos - current position of the piece
        @param direction - direction to move to, in format [x_off, y_off]
        @param side - which side the piece is: WHITE or BLACK
        @return a Move() object which describes the next move of current piece
        '''
        for dis in range(1, 8):
            movement = C(dis * direction[X], dis * direction[Y])
            new_pos = pos + movement
            if self.board.is_valid_pos(new_pos):
                piece_at_pos = self.board.get_piece_at_pos(new_pos)
                if piece_at_pos is None:
                    yield Move(self, new_pos)

                elif piece_at_pos is not None:
                    if piece_at_pos.side != side:
                        yield Move(self, new_pos, piece_to_capture=piece_at_pos)
                    return

    def __eq__(self, other):
        if self.board == other.board and \
           self.side == other.side and \
           self.position == other.position and \
           self.__class__ == other.__class__:
            return True
        return False

    def copy(self):
        cpy = self.__class__(self.board, self.side, self.position,
                             movesMade=self.movesMade)
        return cpy
