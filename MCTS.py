import random

import numpy as np
import chess
import Player
import math

class MCTSPlayer(Player.Player):
    def __init__(self, max_iter=10):
        super().__init__()
        self.c = 1.5
        self.root = None
        self.maxIter = max_iter
        self.exploreMoves = 3

    def nextMove(self, board):
        return board.uci(self.MCTS_choice(board))
    def ucb(self, cur):
        n = cur.Nt if cur.Nt != 0 else .00000000000000000001
        N = cur.parent.Nt if cur.parent.Nt != 0 else 1
        v = cur.Qt + self.c * math.sqrt(math.log(N)/n)
        return v

    def select(self, cur):
        if cur.board.turn:
            return self.selectMax(cur)
        return self.selectMin(cur)

    def selectMax(self, cur):
        ucbMax = -math.inf
        best = None
        for move in cur.children:
            i = cur.children[move]
            v = self.ucb(i)
            if v > ucbMax:
                ucbMax = v
                best = i
        return best
    def selectMin(self, cur):
        ucbMin = math.inf
        best = None
        for move in cur.children:
            i = cur.children[move]
            v = self.ucb(i)
            if v < ucbMin:
                ucbMin = v
                best = i
        return best

    def expand(self, cur):
        if not cur.children:
            for move in cur.board.legal_moves:
                n = Node(cur, move, chess.Board(cur.board.fen()))
                n.board.push_san(cur.board.san(move))
                cur.children[cur.board.uci(move)] = n
            return cur.children[random.choice(list(cur.children.keys()))]
        nPrime = self.select(cur)
        return self.expand(nPrime)
    def explore(self, cur):
        outcome = cur.board.outcome()
        if cur.board.outcome() is not None:
            if outcome.termination == chess.Termination.CHECKMATE:
                v = 1 if outcome.winner == self.player else -1
                return v,cur
            return .5, cur


        return self.explore(self.expand(cur))

    def backPropogate(self, cur, reward):
        if cur is None:
            return
        cur.Nt += 1
        cur.Qt += reward
        self.backPropogate(cur.parent, reward)

    def MCTS_choice(self, board):
        if self.root is None:
            self.root = Node(None, None, chess.Board(board.fen()))
        else:
            prev = board.pop()
            board.push_san(board.san(prev))
            if board.uci(prev) in self.root.children.keys():
                print("exists")
                self.root = self.root.children[board.uci(prev)]
            else:
                self.root = Node(None, None, chess.Board(board.fen()))
        for move in self.root.board.legal_moves:
            n = Node(self.root, move, chess.Board(self.root.board.fen()))
            n.board.push_san(self.root.board.san(move))
            self.root.children[board.uci(move)] = n

        for i in  range(self.maxIter):
            best = self.select(self.root)
            child = self.expand(best)
            for i in range(self.exploreMoves):
                reward,leaf = self.explore(child)
                self.backPropogate(leaf, reward)
            #print(str(self.root))
        self.root = self.select(self.root)
        return self.root.move


class Node():
    def __init__(self, parent, move, board):
        self.parent = parent
        self.move = move
        self.board = board
        self.children = dict()
        self.Qt = 0
        self.Nt = 0
    def __repr__(self):
        return f"{self.board.uci(self.move)}, Qt:{self.Qt}, Nt:{self.Nt}"
    def __str__(self):
        s = ""
        for i in self.children:
            s += self.children[i].__repr__() + "\n"
        s += "\n"
        return s