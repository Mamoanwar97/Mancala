import numpy as np


class Board:
    def __init__(self, board=np.array([[4, 4, 4, 4, 4, 4],[4, 4, 4, 4, 4, 4]]), scores=np.array([0, 0]), last_played_move=-1):
        self.board = board
        self.scores = scores
        self.last_played_move = last_played_move

    def copy(self):
        return Board(np.copy(self.board), np.copy(self.scores), self.last_played_move)


 