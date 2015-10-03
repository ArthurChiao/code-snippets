import re


class InputParser:

    def __init__(self, board, side):
        self.board = board
        self.side = side

    def parse(self, humanInput):
        humanInput = humanInput.lower()
        regexShortNotation = re.compile('[rnbkqp][a-z][1-8]')
        if regexShortNotation.match(humanInput):
            return self.parse_move_code(humanInput)

    def parse_move_code(self, notation):
        '''
        convert move notation code to Move instance
        '''
        moves = self.get_legal_move_codes(self.side)
        for move in moves:
            if move.notation.lower() == notation.lower():
                return move

    def get_move_code(self, move):
        side = self.board.get_move_side(move)
        moves = self.get_legal_move_codes(side)
        for m in moves:
            if m == move:
                return m.notation

    def get_legal_move_codes(self, side):
        '''
        get all legal moves
        '''
        moves = []
        for legal_moves in self.board.get_all_legal_moves(side):
            moves.append(legal_moves)
            legal_moves.notation = self.board.get_move_code(legal_moves)

        valid_moves = self.filter_moves(moves)
        for m in valid_moves:
            m.notation = self.board.get_move_code_with_file(m)

        valid_moves = self.filter_moves(moves)
        for m in valid_moves:
            m.notation = self.board.get_move_code_with_rank(m)

        valid_moves = self.filter_moves(moves)
        for m in valid_moves:
            m.notation = self.board.get_move_code_with_file_rank(m)

        return moves

    def filter_moves(self, moves):
        '''
        filter out invalid moves (invalid notation)
        '''
        return list(filter(lambda move:
            len([m for m in moves if m.notation == move.notation]) > 1, moves))
