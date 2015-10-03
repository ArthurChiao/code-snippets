from Board import Board
from InputParser import InputParser
from AI import AI
import sys
import random

WHITE = True
BLACK = False


def ask_for_player_side():
    side = input("What side would you like to play as [wB]? ").lower()
    if 'w' in side:
        print("You will play as white")
        return WHITE
    else:
        print("You will play as black")
        return BLACK


def ask_for_ai_depth():
    '''
    get AI depth from human input
    '''
    depth = 2
    try:
        depth = int(input("How deep should the AI look for moves?\n"
            "Warning : values above 3 will be very slow. [n]? "))
    except:
        print("Invalid input, defaulting to 2")
    return depth


def print_options():
    undo             = 'u : undo last move'
    show_legal_moves = 'l : show all legal moves'
    random_move      = 'r : make a random move'
    quit             = 'quit : resign'
    move             = 'a3, Nc3, Qxa2, etc : make the move'
    options = [undo, show_legal_moves, random_move, quit, move, '', ]
    print('\n'.join(options))


def print_all_legal_moves(board, parser):
    '''
    print all legal moves, in short-notation format, e.g, a4
    '''
    for move in parser.get_legal_move_codes(board.player):
        print(move.notation)


def get_random_move(board, parser):
    moves = board.get_all_legal_moves(board.player)
    move = random.choice(moves)
    move.notation = parser.get_move_code(move)
    return move


def make_move(move, board):
    print()
    print("Making move : " + move.notation)
    board.make_move(move)


def print_advantage_point(board):
    print("Currently, the point difference is : " +
          str(board.getPointAdvantageOfSide(board.player)))


def undo_last_two_moves(board):
    if len(board.history) >= 2:
        board.undo_last_move()
        board.undo_last_move()


def start_game(board, human, ai):
    parser = InputParser(board, human)
    while True:
        print(board)
        print()
        if board.is_checkmate():
            if board.player == human:
                print("Checkmate, you lost")
            else:
                print("Checkmate! You won!")
            return

        if board.is_stalemate():
            print("Stalemate")

        if board.player == human:
            # print_advantage_point(board)
            move = None
            command = input("It's your move. Type '?' for options. ? ").lower()
            if command == 'u':
                undo_last_two_moves(board)
                continue
            elif command == '?':
                print_options()
                continue
            elif command == 'l':
                print_all_legal_moves(board, parser)
                continue
            elif command == 'r':
                move = get_random_move(board, parser)
            elif command == 'quit':
                return
            else:
                move = parser.parse_move_code(command)
            if move:
                make_move(move, board)
            else:
                print("Couldn't parse input, enter a valid command or move.")

        else:
            print("AI thinking...")
            move = ai.get_best_move()
            move.notation = parser.get_move_code(move)
            make_move(move, board)


if __name__ == '__main__':
    board = Board()

    player_side = ask_for_player_side() # human player color: WHITE or BLACK

    print()
    ai_depth = ask_for_ai_depth()
    ai = AI(board, not player_side, ai_depth)

    try:
        start_game(board, player_side, ai)
    except KeyboardInterrupt:
        sys.exit()
