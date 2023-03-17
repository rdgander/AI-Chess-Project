
import chess
import Player
import MCTS

class Game():
    """Class for running the game of Chess."""
    def __init__(self, player1, player2):
        """Initialize the board and players."""
        # Chess board
        self.board = chess.Board()
        # Player object for white.
        self.white = player1
        self.white.setPlayer(chess.WHITE)
        # Player object for black.
        self.black = player2
        self.black.setPlayer(chess.BLACK)
        # Player object of the players who's turn it is.
        self.current_player = None

    def nextTurn(self):
        """Finds the next move to make based on what
            type of player is the current player"""
        # Selecting the current player based on the boards turn.
        # Maybe has a bug with the minimax player where this is not update
        # which may possibly mess with the minimax move selection.
        self.current_player = self.white if self.board.turn else self.black
        # Variable to hold the move to make.
        move = None
        while True:
            print("\n" + str(self.board))
            print(self.white.heuristic(self.board))
            # Get the next move the player wants to make.
            moveString = self.current_player.nextMove(self.board)
            try:
                # try converting the move string to a chess.Move object.
                move = chess.Move.from_uci(moveString)
            except ValueError:
                # ValueError is raised when the move is in an invalid format.
                print("\nIncorrect Format, please input moves in uci format such as a2a4\n")
                continue

            # Check if the move is legal.
            # Checks through the list of all legal moves which may be expensive.
            # Improvement would be to check if this specific move is illegal.
            # There may be a method for this in the library.
            if move in self.board.legal_moves:
                # Break out of the loop since the move has been verified.
                break
            # Only makes it here if the legal check fails meaning the move is illegal.
            print("Illegal move")
        # Make the next move on the board.
        self.board.push(move)

    def run(self):
        """Runs the game until termination."""
        # Loop to get the next turn repeatedly until the game is terminated.
        while self.board.outcome() is None:
            self.nextTurn()
        # The outcome of the game, a chess.Outcome object.
        outcome = self.board.outcome()
        print("\n" + str(self.board) + "\n")

        # Checks if the type of termination is checkmate.
        if outcome.termination.value == chess.Termination.CHECKMATE:
            # Checks who one and prints out the winner.
            print("White" if outcome.winner else "Black", "Checkmate")
        else:
            # Prints the type of termination if it is not checkmate.
            print(outcome.termination.name)

if __name__ == '__main__':
    player2 = MCTS.MCTSPlayer(3)
    player1 = Player.RandomPlayer()
    #player2 = Player.MMPlayer(5)
    Game(player1,player2).run()