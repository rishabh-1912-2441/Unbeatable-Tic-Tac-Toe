"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = sum(row.count(X) for row in board)
    o_counter = sum(row.count(O) for row in board)
    if x_counter <= o_counter: 
        return X
    else : 
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                all_possible_actions.add((i,j))

    return all_possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    if board[i][j]!= EMPTY:
        raise Exception ("Invalid Move:Cell already acquired")
    player_turn = player(board)
    new_board = [row.copy() for row in board]
    new_board[i][j] = player_turn
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #checking in rows

    for row in board:
        if all(box == X for box in row):
            return X
        elif all(box == O for box in row):
            return O
        
    # checking in columns 

    for i in range(3):
        if all(board[j][i] == X for j in range(3)):
            return X
        elif all(board[j][i] == O for j in range(3)):
            return O
        
    # checking for diagonals 

    if all(board[i][i] == X for i in range(3)) or all(board[i][2-i] == X for i in range(3)):
        return X
    if all(board[i][i] == O for i in range(3)) or all(board[i][2-i] == O for i in range(3)):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)!= None or all(all(box!=EMPTY for box in row) for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if terminal(board):
        if winner_player == X:
            return 1
        elif winner_player == O:
            return -1
        else:
            return 0


"""
Without Alpha-Beta pruning
"""

# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """

#     if terminal(board):
#         return None

#     player_turn = player(board)
#     if player_turn == X:
#         best_score = -math.inf
#         best_move = None
#         for action in actions(board): #Move taken by X 
#             #Produces highest values of the minimum value of (board,action)
#             new_score = min_value(result(board, action)) 
#             if new_score > best_score:
#                 best_score = new_score
#                 best_move = action
#         return best_move
#     else:
#         best_score = math.inf
#         best_move = None
#         for action in actions(board): #Move taken by O 
#             #Produces lowest values of the maximum value of (board,action)
#             new_score = max_value(result(board, action))
#             if new_score < best_score:
#                 best_score = new_score
#                 best_move = action
#         return best_move

# def max_value(board):
#     if terminal(board):
#         return utility(board)
#     v = -math.inf
#     for action in actions(board):
#         v = max(v, min_value(result(board, action)))
#     return v


# def min_value(board):
#     if terminal(board):
#         return utility(board)
#     v = math.inf
#     for action in actions(board):
#         v = min(v, max_value(result(board, action)))
#     return v

"""
With Alpha-Beta pruning
"""
def minimax(board):
    """
    Returns the optimal action for the current player on the board using alpha-beta pruning.
    """
    if terminal(board):
        return None

    player_turn = player(board)
    if player_turn == X:
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            new_score = min_value(result(board, action), alpha, beta)
            if new_score > best_score:
                best_score = new_score
                best_move = action
            alpha = max(alpha, best_score)
        return best_move
    else:
        best_score = math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            new_score = max_value(result(board, action), alpha, beta)
            if new_score < best_score:
                best_score = new_score
                best_move = action
            beta = min(beta, best_score)
        return best_move

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
