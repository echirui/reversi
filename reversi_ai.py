import subprocess
from time import sleep

import reversi
from reversi import W,B,EMPTY,GRIDS,CONVERT_DICT,convert_kifu,list_direct,re_input_check
import random
from copy import copy

class AIPlayer(reversi.Player):
    def __init__(self, color):
        self.rv = reversi.Reversi(color)
        super().__init__(color)

    def input_board(self, board):
        self.rv = reversi.Reversi(board)
        self.rv.player = self.color

    def output_board(self):
        self.rv.clear_suggest()
        self.rv.check_pass()
        return self.rv.suggest[random.randint(0,len(self.rv.suggest)-1)]


class AIWrapper(reversi.Player):
    def __init__(self, color):
        self.rv = reversi.Reversi(color)
        self.ps = subprocess.Popen('env python3 ai.py'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        super().__init__(color)

    def __del__(self):
        self.ps.kill()

    def input_board(self, board):
        stdin = str(self.rv.player) + '\n'
        for i in range(GRIDS):
            stdin += ' '.join(map(str, board[i])) + '\n'
        #print(stdin)
        self.ps.stdin.write(stdin.encode('utf-8'))
        self.ps.stdin.flush()
        return super().input_board(board)

    def output_board(self):
        return [int(i) for i in self.ps.stdout.readline().strip().split()]


if __name__ == '__main__':
    pass