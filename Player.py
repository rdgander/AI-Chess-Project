import math
import random

import chess

class Player():
    """Base Class for player objects."""
    def __init__(self):
        """Initialize the values of the player"""
        # The max score that the player can have.
        # Represents a win for the player.
        self.WINSCORE = 39
        # The minimum score that the player can have.
        # Represents a loss for the player.
        self.LOSESCORE = -39
        # Represents a tie.
        self.TIESCORE = 0

        # chess.Color Enum of which color the player is.
        self.player = None

    def setPlayer(self, player):
        self.player = player

    def nextMove(self, board):
        """Find the next move for the player"""
        pass

    def heuristic(self, board):
        """Basic heuristic for the board state."""


        s = 0
        # iterates through all of the squares on the board.
        # Adds the cost of the players pieces.
        # Subtracts the cost of the opponent pieces.
        for square in range(64):
            piece = board.piece_at(square)
            if piece is None:
                continue
            value = 0
            if piece.piece_type == chess.PAWN:
                value = 1
            elif piece.piece_type == chess.KNIGHT:
                value = 3
            elif piece.piece_type == chess.BISHOP:
                value = 3
            elif piece.piece_type == chess.ROOK:
                value = 5
            elif piece.piece_type == chess.QUEEN:
                value = 9
            if piece.color == self.player:
                s += value
            else:
                s -= value
        return s

class ManualPlayer(Player):
    """A Manual Player to be controlled by a human."""
    def __init__(self):
        super().__init__()

    def nextMove(self, board):
        """Takes the move in as input from the player."""
        move = input("Input a Move:\n")
        return move

class AutoCheckMatePlayer(Player):
    """A Player that makes the moves of fool's mate for testing purposes.
        Only works if both players are objects of this class."""
    # The series of moves to be made for fool's mate.
    moves = ["f2f3", "e7e6", "g2g4", "d8h4"]
    def __init__(self):
        super().__init__()

    def nextMove(self, board):
        # Reset the list of moves to work for a further game.
        # Currently the program only runs one game.
        if not AutoCheckMatePlayer.moves:
            AutoCheckMatePlayer.moves = ["f2f3", "e7e6", "g2g4", "d8h4"]
        # Pop's the first move from the list.
        return AutoCheckMatePlayer.moves.pop(0)

class SearchingPlayer(Player):
    """Parent class for all search related automated players."""
    def __init__(self, maxDepth=3):
        super().__init__()
        # The maxDepth to be searched.
        self.maxDepth = maxDepth

class MMPlayer(SearchingPlayer):
    """Class for a minimax driven player."""
    def __init__(self, maxDepth=3):
        super().__init__(maxDepth)
    def nextMove(self,board):
        # Call max on the board since it is this players turn.
        move,value = self.maxValue(board, 0, -math.inf, math.inf)
        return board.uci(move)

    def minValue(self,board, depth, alpha, beta):
        """Min step of minimax"""
        # Checks for terminal state.
        terminal = self.terminal(board)
        # terminal[0] is a boolean indicating if the state is terminal.
        if terminal[0]:
            # terminal[1] is the value of the terminal state.
            return None, terminal[1]
        # Depth check.
        if depth >= self.maxDepth:
            # returns the heuristic value of the board.
            return None, self.heuristic(board)
        v = math.inf
        bestMove = None
        for move in board.legal_moves:
            # Make the move.
            board.push(move)
            # Run max on the new board.
            vprime = self.maxValue(board, depth + 1, alpha, beta)[1]
            # Undo the move.
            board.pop()
            # Check if the new value is less than the previous value.
            if vprime < v:
                # Assign the new value to v.
                v = vprime
                # Assign the move as the bestMove
                bestMove = move
            beta = min(beta, v)
            # Pruning check.
            if alpha >= beta:
                return bestMove, v
        return bestMove, v

    def maxValue(self, board, depth, alpha, beta):
        """Max step of minimax"""
        # Checks for terminal state.
        terminal = self.terminal(board)
        # terminal[0] is a boolean indicating if the state is terminal.
        if terminal[0]:
            # terminal[1] is the value of the terminal state.
            return None, terminal[1]
        # Depth check.
        if depth >= self.maxDepth:
            # returns the heuristic value of the board.
            return None, self.heuristic(board)

        v = -math.inf
        bestMove = None
        for move in board.legal_moves:
            # Make the move.
            board.push(move)
            # Run min on the new board.
            vprime = self.minValue(board,depth +1,alpha,beta)[1]
            # Undo the move.
            board.pop()
            # Check if the new value is greater than the previous value.
            if vprime > v:
                # Assign the new value to v.
                v = vprime
                # Assign the move as the bestMove
                bestMove = move
            alpha = max(alpha, v)
            # Pruning check.
            if alpha >= beta:
                return bestMove, v
        return bestMove, v

    def terminal(self, board):
        """Return if the board is terminal and what the value is."""
        # Termination check.
        if board.outcome() is not None:
            # Check if the terminal state is checkmate.
            if board.outcome().termination.value == chess.Termination.CHECKMATE:
                # Check if the player won.
                if board.outcome().winner == self.player:
                    # return that the state is terminal and the value is the win score.
                    return True, self.WINSCORE
                # return that the state is terminal and the value is the lose score.
                return True, self.LOSESCORE
            # return that the state is terminal and the value is the tie score.
            return True, self.TIESCORE
        # return that the state is not terminal
        # The value only matters if it is terminal, so return a null value.
        return False, None
class RandomPlayer(Player):
    def __init__(self):
        super().__init__()
    def nextMove(self, board):
        return board.uci(random.choice(list(board.legal_moves)))
