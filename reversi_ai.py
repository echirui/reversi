import subprocess
from time import sleep

import reversi
from reversi import W,B,EMPTY,GRIDS,CONVERT_DICT,convert_kifu,list_direct,re_input_check
import random
from copy import copy

class AIPlayer(reversi.Player):
    rv = None
    def __init__(self, color, board):
        self.rv = reversi.Reversi(copy(board))
        super().__init__(color)

    def input_board(self, board):
        self.rv = reversi.Reversi(copy(board))
        self.rv.player = self.color
        return super().input_board(board)

    def output_board(self):
        self.rv.clear_suggest()
        self.rv.check_pass()
        return self.rv.suggest[random.randint(0,len(self.rv.suggest)-1)]


class AIWrapper(reversi.Player):
    rv = None
    def __init__(self, color, board):
        self.rv = reversi.Reversi(color)
        self.rv.board = board
        self.ai = subprocess.Popen('env python3 ai.py'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        super().__init__(color)

    def __del__(self):
        self.ai.kill()

    def input_ai_board(self, board):
        stdin = str(self.rv.player) + '\n'
        for i in range(GRIDS):
            stdin += ' '.join(map(str, board[i])) + '\n'
        #print(stdin)
        self.ai.stdin.write(stdin.encode('utf-8'))
        self.ai.stdin.flush()
        return super().input_board(board)

    def output_ai_board(self):
        x, y = [int(i) for i in self.ai.stdout.readline().decode().strip().split()]
        return x, y


if __name__ == '__main__':
    pass