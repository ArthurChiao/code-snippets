from Board import Board
from MoveNode import MoveNode
from InputParser import InputParser
import copy
import random
from multiprocessing import Pool


WHITE = True
BLACK = False


class AI:

    depth = 1
    board = None
    side = None
    num_analyzed_moves = 0

    def __init__(self, board, side, depth):
        self.board = board
        self.side = side
        self.depth = depth
        self.parser = InputParser(self.board, self.side)

    def getFirstMove(self, side):
        move = list(self.board.get_all_legal_moves(side))[0]
        return move

    def getAllMovesLegalConcurrent(self, side):
        p = Pool(8)
        unfilteredMovesWithBoard = \
            [(move, copy.deepcopy(self.board))
             for move in self.board.getAllMovesUnfiltered(side)]
        legal_moves = p.starmap(self.returnMoveIfLegal,
                               unfilteredMovesWithBoard)
        p.close()
        p.join()
        return list(filter(None, legal_moves))

    def minChildrenOfNode(self, node):
        lowestNodes = []
        for child in node.children:
            if not lowestNodes:
                lowestNodes.append(child)
            elif child < lowestNodes[0]:
                lowestNodes = []
                lowestNodes.append(child)
            elif child == lowestNodes[0]:
                lowestNodes.append(child)
        return lowestNodes

    def maxChildrenOfNode(self, node):
        highestNodes = []
        for child in node.children:
            if not highestNodes:
                highestNodes.append(child)
            elif child < highestNodes[0]:
                highestNodes = []
                highestNodes.append(child)
            elif child == highestNodes[0]:
                highestNodes.append(child)
        return highestNodes

    def _populate_child_nodes(self, node):
        node.advantage_points = self.board.get_advantage_points(self.side)
        node.depth = node.get_depth()
        if node.depth == self.depth:
            return

        side = self.board.player # which side is in turn to play

        legal_moves = self.board.get_all_legal_moves(side)
        if not legal_moves:
            if self.board.is_checkmate():
                node.move.checkmate = True
                return
            elif self.board.is_stalemate():
                node.move.stalemate = True
                node.advantage_points = 0
                return
            raise Exception()

        for move in legal_moves:
            self.num_analyzed_moves += 1
            node.children.append(MoveNode(move, [], node))
            self.board.make_move(move)
            self._populate_child_nodes(node.children[-1])
            self.board.undo_last_move()

    def _gen_move_tree(self):
        '''
        get AI's entire move tree in current status
        '''
        move_tree = []
        for move in self.board.get_all_legal_moves(self.side):
            move_tree.append(MoveNode(move, [], None))

        for node in move_tree:
            self.board.make_move(node.move)
            self._populate_child_nodes(node)
            self.board.undo_last_move()
        return move_tree

    def _get_advantage_points(self, node):
        '''
        get AI's advantage points over human
        '''
        if node.children:
            for child in node.children:
                child.advantage_points = self._get_advantage_points(child)

            # If the depth is divisible by 2,
            # it's a move for the AI's side, so return max
            if node.children[0].depth % 2 == 1:
                return(max(node.children).advantage_points)
            else:
                return(min(node.children).advantage_points)
        else:
            return node.advantage_points

    def _get_best_move(self, move_tree):
        '''
        get best move with the given move tree

        You should not call this function directly, instead, call the wrapper
        function get_best_move(self)
        '''
        best_nodes = [] # best move nodes
        for node in move_tree:
            node.advantage_points = self._get_advantage_points(node)
            if not best_nodes:
                best_nodes.append(node)
            elif node > best_nodes[0]:
                best_nodes = []
                best_nodes.append(node)
            elif node == best_nodes[0]:
                best_nodes.append(node)

        return [node.move for node in best_nodes]

    def get_best_move(self):
        '''
        get AI's best move in current status
        '''
        move_tree = self._gen_move_tree()
        best_moves = self._get_best_move(move_tree)
        rand_best_move = random.choice(best_moves)
        rand_best_move.notation = self.parser.get_move_code(rand_best_move)
        return rand_best_move

    def make_best_move(self):
        self.board.make_move(self.get_best_move())

    def _is_valid_move(self, move, side):
        for m in self.board.get_all_legal_moves(side):
            if move == m:
                return True
        return False

    def get_random_move(self):
        '''
        get a random move from all legal moves
        '''
        moves = list(self.board.get_all_legal_moves(self.side))
        return random.choice(moves)

    def make_random_move(self):
        '''
        AI makes a random move for next step
        '''
        moveToMake = self.get_random_move()
        self.board.make_move(moveToMake)


if __name__ == "__main__":
    mainBoard = Board()
    ai = AI(mainBoard, True, 3)
    print(mainBoard)
    ai.make_best_move()
    print(mainBoard)
    print(ai.num_analyzed_moves)
    print(mainBoard.movesMade)
