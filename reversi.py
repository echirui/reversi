#!/usr/bin/env python3
# coding: utf-8

import re
import sys

GRIDS = 8
EMPTY = 0    # 2bit 0b00
B = 1    # 2bit 0b01
W = 2    # 2bit 0b10
MASK = 0b11 # and enable flag 2bit 0b11

CONVERT_DICT = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
# [R, D, L, U, RU, RD, LD, LU]
list_direct_x = [1, 0, -1, 0, 1, 1, -1, -1]
list_direct_y = [0, 1, 0, -1, -1, 1, 1, -1]
list_direct = [[x,y] for x, y in zip(list_direct_x, list_direct_y)]

# check 0x0 0x1 ... 7x6 7x7
re_input_check = re.compile(r"""^[0-7][0-7]$""")

# check a1 a2 ... h7 h8
re_input_sd_check = re.compile(r"""^[a-h][1-8]$""")

inputs = {1:"Black:", 2:"White:"}

class Player:
    """reversi player. AI or Person"""
    color = ""

    def __init__(self, color):
        # B(1) or W(2)
        self.color = color

    def is_myturn(self, color):
        return self.color == color

    def input_board(self, board):
        """
        """
        pass

    def output_board(self):
        for _ in range(10):
            # repeat 10 times. exit() if over
            try:
                move = input(inputs[self.color])
                if move in ['exit','q','quit']:
                    break
                if not re_input_check.match(move):
                    self.message(-1, f'Error incorrect input: {move}')
                    continue
                else:
                    break
            except:
                print('Error incorrect input')
                exit()
        else:
            # repeat over 10 times error.
            exit()

        return [int(i) for i in move]


class Reversi:
    """
    """
    #properties
    suggest = list()
    pass_flag = 0
    ui = list()

    def __init__(self, board=None):
        self.num_stones = [None, 2, 2]
        if board:
            self.board = board
        else:
            self.board = [[EMPTY for _ in range(GRIDS)] for _ in range(GRIDS)]
            self.board[4][3] = 1
            self.board[3][4] = 1
            self.board[3][3] = 2
            self.board[4][4] = 2
        self.player = B # first turn (1:black 2:white)
        self.kifu = list()

    @staticmethod
    def is_inside(x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    @staticmethod
    def is_empty(x, y, board):
        return not (board[x][y] == B or board[x][y] == W)

    def check(self, x, y, dx, dy):
        length = 0
        nx, ny = x, y
        for i in range(1, GRIDS):
            nx = nx + dx
            ny = ny + dy
            if not is_inside(nx, ny):
                return 0
            if is_empty(nx, ny, self.board):
                return 0
            if self.board[nx][ny] == (self.player^MASK):
                length += 1
            elif self.board[nx][ny] == self.player:
                return length
        else:
            return 0

    def flip(self, x, y, dx, dy, length):
        for i in range(1,length+1):
            self.swap(x+dx*i,y+dy*i)
        return

    def swap(self, x, y):
        self.num_stones[self.player] += 1
        self.num_stones[self.player^MASK] -= 1
        self.board[x][y] = self.board[x][y] ^ MASK
        return

    def put(self, x, y):
        """ put stone. And check illegal.
        """
        # check illegal move
        if not self.is_inside(x, y):
            self.message("x or y is out of range", -1)
            return False
        if not self.is_empty(x, y, self.board):
            self.message(f"already stone exists: {x},{y}", -1)
            return False
        if not [x, y] in self.suggest:
            self.message(f'Error incorrect move: {x},{y}', 2)
            return False
        # put stone
        self.board[x][y] = self.player
        self.kifu.append(str(x)+str(y))
        self.num_stones[self.player] += 1

        self.clear_suggest()
        # check 8 direction. and turn the stone upside down.
        for dx, dy in list_direct:
            length = self.check(x, y, dx, dy)
            if length:
                self.flip(x, y, dx, dy, length)

        return True

    def turn_next(self):
        """
        """
        # 01 xor 11 = 10, 10 xor 11 = 01
        self.player = self.player ^ MASK
        return

    def end(self):
        """
        """
        if self.num_stones[B]+self.num_stones[W] == GRIDS*GRIDS:
            return True
        if self.num_stones[B] == 0:
            return True
        if self.num_stones[W] == 0:
            return True
        if self.pass_flag == 2:
            # double pass
            return True
        return False

    def check_pass(self):
        not_empty__ = [[i, j] for i in range(GRIDS) for j in range(GRIDS) if is_empty(i, j, self.board)]
        return_flag = True
        for x, y in not_empty__:
            for dx, dy in list_direct:
                if self.check(x, y, dx, dy) != 0:
                    return_flag = False
                    self.board[x][y] = MASK
                    if not [x, y] in self.suggest:
                        self.suggest.append([x, y])
        return return_flag

    def clear_suggest(self):
        for x, y in self.suggest:
            if self.board[x][y] == MASK:
                self.board[x][y] = EMPTY
        self.suggest = list()
        return

    @staticmethod
    def win_reason(s):
        if s[B] > s[W]:
            return "Black won!"
        elif s[B] < s[W]:
            return "White won!"
        else:
            #s[B] == s[W]:
            return "Draw!"

    @staticmethod
    def convert_kifu(ki):
        list_return = list()
        for i in range(0, len(ki), 2):
            list_return.append([CONVERT_DICT[ki[i]], int(ki[i+1])-1])
        return list_return

    def score(self):
        return f"Score[B:{self.num_stones[B]}, W:{self.num_stones[W]}]"

    def output(self):
        """
        """
        def rep(x):
            """Inner function. replace board[][] to strings.
            """
            if x == 0:
                return ' .'
            elif x == 1:
                return ' ○'
            elif x == 2:
                return ' ●'
            else: # x == 3
                return ' x'
        # header
        self.ui = [self.score()]
        self.ui.append('    ' + ' '.join([str(x) for x in range(GRIDS)]))
        # board
        for i in range(GRIDS):
            self.ui.append(str(i) + '0 ' + ''.join(map(rep, self.board[i])))
        print(*self.ui, sep='\n')

    @staticmethod
    def message(message="Error message",code=0):
        if code:
            print(f"{message} {code=}")
        else:
            print(message)


# static fucntion
is_inside = Reversi.is_inside
is_empty = Reversi.is_empty
convert_kifu = Reversi.convert_kifu
message = Reversi.message
win_reason = Reversi.win_reason