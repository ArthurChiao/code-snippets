from Pawn import Pawn
from Rook import Rook
from King import King
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from Coordinate import Coordinate as C
from termcolor import colored

from Move import Move

WHITE = True
BLACK = False


class Board:

    def __init__(self, mateInOne=False, castleBoard=False,
                 pessant=False, promotion=False):
        self.pieces = []
        self.history = []
        self.points = 0
        self.player = WHITE
        self.move_count = 0
        self.checkmate = False

        if not mateInOne and not castleBoard and not pessant and not promotion:
            self.pieces.extend([Rook(self, BLACK, C(0, 7)),
                                Knight(self, BLACK, C(1, 7)),
                                Bishop(self, BLACK, C(2, 7)),
                                Queen(self, BLACK, C(3, 7)),
                                King(self, BLACK, C(4, 7)),
                                Bishop(self, BLACK, C(5, 7)),
                                Knight(self, BLACK, C(6, 7)),
                                Rook(self, BLACK, C(7, 7))])
            for x in range(8):
                self.pieces.append(Pawn(self, BLACK, C(x, 6)))
            for x in range(8):
                self.pieces.append(Pawn(self, WHITE, C(x, 1)))
            self.pieces.extend([Rook(self, WHITE, C(0, 0)),
                                Knight(self, WHITE, C(1, 0)),
                                Bishop(self, WHITE, C(2, 0)),
                                Queen(self, WHITE, C(3, 0)),
                                King(self, WHITE, C(4, 0)),
                                Bishop(self, WHITE, C(5, 0)),
                                Knight(self, WHITE, C(6, 0)),
                                Rook(self, WHITE, C(7, 0))])

        elif promotion:
            pawnToPromote = Pawn(self, WHITE, C(1, 6))
            pawnToPromote.movesMade = 1
            kingWhite = King(self, WHITE, C(4, 0))
            kingBlack = King(self, BLACK, C(3, 2))
            self.pieces.extend([pawnToPromote, kingWhite, kingBlack])

        elif pessant:
            pawn = Pawn(self, WHITE, C(1, 4))
            pawn2 = Pawn(self, BLACK, C(2, 6))
            kingWhite = King(self, WHITE, C(4, 0))
            kingBlack = King(self, BLACK, C(3, 2))
            self.pieces.extend([pawn, pawn2, kingWhite, kingBlack])
            self.history = []
            self.player = BLACK
            self.points = 0
            self.move_count = 0
            self.checkmate = False
            firstMove = Move(pawn2, C(2, 4))
            self.make_move(firstMove)
            self.player = WHITE
            return

    def __str__(self):
        return self.decorate_board(self.draw_board(self.pieces))

    def undo_last_move(self):
        lastMove, pieceTaken = self.history.pop()

        if lastMove.queensideCastle or lastMove.kingsideCastle:
            king = lastMove.piece
            rook = lastMove.specialMovePiece

            self._move_piece_to_pos(king, lastMove.old_pos)
            self._move_piece_to_pos(rook, lastMove.rookMove.old_pos)

            king.movesMade -= 1
            rook.movesMade -= 1

        elif lastMove.pessant:
            pawnMoved = lastMove.piece
            pawnTaken = pieceTaken
            self.pieces.append(pawnTaken)
            self._move_piece_to_pos(pawnMoved, lastMove.old_pos)
            pawnMoved.movesMade -= 1
            if pawnTaken.side == WHITE:
                self.points += 1
            if pawnTaken.side == BLACK:
                self.points -= 1

        elif lastMove.promotion:
            pawnPromoted = lastMove.piece
            promotedPiece = self.get_piece_at_pos(lastMove.new_pos)
            self.pieces.remove(promotedPiece)
            self.pieces.append(pawnPromoted)
            if pawnPromoted.side == WHITE:
                self.points -= promotedPiece.value - 1
            elif pawnPromoted.side == BLACK:
                self.points += promotedPiece.value - 1
            pawnPromoted.movesMade -= 1

        else:
            pieceToMoveBack = lastMove.piece
            self._move_piece_to_pos(pieceToMoveBack, lastMove.old_pos)
            if pieceTaken:
                if pieceTaken.side == WHITE:
                    self.points += pieceTaken.value
                if pieceTaken.side == BLACK:
                    self.points -= pieceTaken.value
                self.addPieceToPosition(pieceTaken, lastMove.new_pos)
                self.pieces.append(pieceTaken)
            pieceToMoveBack.movesMade -= 1

        self.player = not self.player

    def is_checkmate(self):
        if len(self.get_all_legal_moves(self.player)) == 0:
            for move in self.getAllMovesUnfiltered(not self.player):
                piece_to_kill = move.piece_to_capture
                if piece_to_kill and piece_to_kill.stringRep == "K":
                    return True
        return False

    def is_stalemate(self):
        if len(self.get_all_legal_moves(self.player)) == 0:
            for move in self.getAllMovesUnfiltered(not self.player):
                piece_to_kill = move.piece_to_capture
                if piece_to_kill and piece_to_kill.stringRep == "K":
                    return False
            return True
        return False

    def getLastMove(self):
        if self.history:
            return self.history[-1][0]

    def getLastPieceMoved(self):
        if self.history:
            return self.history[-1][0].piece

    def _add_move_to_history(self, move):
        '''
        add (Move, killed Piece) pair to history
        '''
        killed_piece = None
        if move.pessant:
            killed_piece = move.specialMovePiece
            self.history.append([move, killed_piece])
            return
        killed_piece = move.piece_to_capture
        if killed_piece:
            self.history.append([move, killed_piece])
            return

        self.history.append([move, None])

    def getCurrentSide(self):
        return self.player

    def draw_board(self, pieces):
        '''
        draw a new board with the states of the pieces

        @param pieces - all live pieces on the board
        @return the drawn board (in String format)
        '''
        display_board = ''
        for y in range(7, -1, -1):
            for x in range(8):
                piece = None
                for p in pieces:
                    if p.position == C(x, y):
                        piece = p
                        break
                pieceRep = ''
                if piece:
                    side = piece.side
                    color = 'blue' if side == WHITE else 'red'
                    pieceRep = colored(piece.stringRep, color)
                else:
                    pieceRep = 'x'
                display_board += pieceRep + ' '
            display_board += '\n'
        display_board = display_board.strip()
        return display_board

    def decorate_board(self, board_str):
        '''
        add some decorations to the text-format-board
        e.g. wrap the board with number-index and alphabetic-index

        @param board_str - board to be displayed, in string format
        @return decorated board for better displaying, in string format
        '''
        decorated_board = '\n'.join(
            ['   a b c d e f g h   ', ' '*21] +
            ['%d  %s  %d' % (8-r, s.strip(), 8-r)
             for r, s in enumerate(board_str.split('\n'))] +
            [' '*21, '   a b c d e f g h   ']
            ).rstrip()
        return decorated_board

    def get_piece_rank(self, piece):
        '''
        @return rank (row) the piece is on, range [0-7]
        '''
        return str(piece.position[1] + 1)

    def get_piece_file(self, piece):
        '''
        @return file (column) the piece is on, range [a-h]
        '''
        transTable = str.maketrans('01234567', 'abcdefgh')
        return str(piece.position[0]).translate(transTable)

    def get_move_code(self, move):
        '''
        get the move's repsentation code
        '''
        notation = ""
        piece_to_move = move.piece
        piece_to_kill = move.piece_to_capture

        if move.queensideCastle:
            return "0-0-0"

        if move.kingsideCastle:
            return "0-0"

        if piece_to_move.stringRep != 'p':
            notation += piece_to_move.stringRep

        if piece_to_kill is not None:
            if piece_to_move.stringRep == 'p':
                notation += self.get_piece_file(piece_to_move)
            notation += 'x'

        notation += self.coordinate_itoh(move.new_pos)

        if move.promotion:
            notation += "=" + str(move.specialMovePiece.stringRep)

        return notation

    def get_move_code_with_file(self, move):
        # TODO: Use self.get_move_code instead of repeating code
        notation = ""
        piece_to_move = self.get_piece_at_pos(move.old_pos)
        piece_to_kill = self.get_piece_at_pos(move.new_pos)

        if piece_to_move.stringRep != 'p':
            notation += piece_to_move.stringRep
            notation += self.get_piece_file(piece_to_move)

        if piece_to_kill is not None:
            notation += 'x'

        notation += self.coordinate_itoh(move.new_pos)
        return notation

    def get_move_code_with_rank(self, move):
        # TODO: Use self.get_move_code instead of repeating code
        notation = ""
        piece_to_move = self.get_piece_at_pos(move.old_pos)
        piece_to_kill = self.get_piece_at_pos(move.new_pos)

        if piece_to_move.stringRep != 'p':
            notation += piece_to_move.stringRep
            notation += self.get_piece_rank(piece_to_move)

        if piece_to_kill is not None:
            notation += 'x'

        notation += self.coordinate_itoh(move.new_pos)
        return notation

    def get_move_code_with_file_rank(self, move):
        # TODO: Use self.get_move_code instead of repeating code
        notation = ""
        piece_to_move = self.get_piece_at_pos(move.old_pos)
        piece_to_kill = self.get_piece_at_pos(move.new_pos)

        if piece_to_move.stringRep != 'p':
            notation += piece_to_move.stringRep
            notation += self.get_piece_file(piece_to_move)
            notation += self.get_piece_rank(piece_to_move)

        if piece_to_kill is not None:
            notation += 'x'

        notation += self.coordinate_itoh(move.new_pos)
        return notation
        return

    def coordinate_htoi(self, coord):
        '''
        convert position/coordinate from human-natural representation to
        integer representation, eg. [1,1] -> b2

        @param coord - coordinate/position in human-natural representation
        @return equivalent coordinate/position in integer X,Y format
        '''
        transTable = str.maketrans('abcdefgh', '12345678')
        coord = coord.translate(transTable)
        coord = [int(c)-1 for c in coord]
        pos = C(coord[0], coord[1])
        return pos

    def coordinate_itoh(self, pos):
        '''
        convert position/coordinate from integer representation to human
        representation, eg. [1,1] -> b2

        @param pos - coordinate/position in integer X,Y format
        @return equivalent human-natural representation
        '''
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1]+1)
        return notation

    def is_valid_pos(self, pos):
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        else:
            return False

    def get_move_side(self, move):
        '''
        which side (WHITE or BLACK) is running this move
        '''
        return move.piece.side

    def get_piece_position(self, piece):
        for y in range(8):
            for x in range(8):
                if self.boardArray[y][x] is piece:
                    return C(x, 7-y)

    def get_piece_at_pos(self, pos):
        for piece in self.pieces:
            if piece.position == pos:
                return piece

    def _move_piece_to_pos(self, piece, pos):
        piece.position = pos

    def addPieceToPosition(self, piece, pos):
        piece.position = pos

    def clearPosition(self, pos):
        x, y = self.coordToLocationInArray(pos)
        self.boardArray[x][y] = None

    def coordToLocationInArray(self, pos):
        return (7-pos[1], pos[0])

    def locationInArrayToCoord(self, loc):
        return (loc[1], 7-loc[0])

    def make_move(self, move):
        self._add_move_to_history(move)
        if move.kingsideCastle or move.queensideCastle:
            kingToMove = move.piece
            rookToMove = move.specialMovePiece
            self._move_piece_to_pos(kingToMove, move.new_pos)
            self._move_piece_to_pos(rookToMove, move.rookMovePos)
            kingToMove.movesMade += 1
            rookToMove.movesMade += 1

        elif move.pessant:
            pawnToMove = move.piece
            pawnToTake = move.specialMovePiece
            pawnToMove.position = move.new_pos
            self.pieces.remove(pawnToTake)
            pawnToMove.movesMade += 1

        elif move.promotion:
            self.pieces.remove(move.piece)
            self.pieces.append(move.specialMovePiece)
            if move.piece.side == WHITE:
                self.points += move.specialMovePiece.value - 1
            if move.piece.side == BLACK:
                self.points -= move.specialMovePiece.value - 1

        else:
            piece_to_move = move.piece
            piece_to_kill = move.piece_to_capture

            if piece_to_kill:
                if piece_to_kill.side == WHITE:
                    self.points -= piece_to_kill.value
                if piece_to_kill.side == BLACK:
                    self.points += piece_to_kill.value
                self.pieces.remove(piece_to_kill)

            self._move_piece_to_pos(piece_to_move, move.new_pos)
            piece_to_move.movesMade += 1
        self.move_count += 1
        self.player = not self.player # switch players in turn

    def get_points(self, side):
        '''
        get the score/points of given side
        '''
        points = 0
        for piece in self.pieces:
            if piece.side == side:
                points += piece.value
        return points

    def get_advantage_points(self, side):
        '''
        how much points/score the given side is ahead of the other side
        '''
        advantages = self.get_points(side) - self.get_points(not side)
        return advantages

    def getAllMovesUnfiltered(self, side, includeKing=True):
        unfilteredMoves = []
        for piece in self.pieces:
            if piece.side == side:
                if includeKing or piece.stringRep != 'K':
                    for move in piece.get_possible_moves():
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side):
        for move in self.getAllMovesUnfiltered(side):
            piece_to_kill = move.piece_to_capture
            if piece_to_kill and piece_to_kill.stringRep == 'K':
                return False
        return True

    def moveIsLegal(self, move):
        side = move.piece.side
        self.make_move(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undo_last_move()
        return isLegal

    # TODO: remove side parameter, unneccesary
    def get_all_legal_moves(self, side):
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        legalMoves = []
        for move in unfilteredMoves:
            if self.moveIsLegal(move):
                legalMoves.append(move)
        return legalMoves
