﻿#!/usr/bin/env python3
# coding: utf-8

import re
import sys

GRIDS = 8
EMPTY = 0    # 2bit 0b00
B = 1    # 2bit 0b01
W = 2    # 2bit 0b10
MASK = 0b11 # and enable flag 2bit 0b11

CONVERT_DICT = {'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7'}
# [R, D, L, U, RU, RD, LD, LU]
list_direct_x = [1, 0, -1, 0, 1, 1, -1, -1]
list_direct_y = [0, 1, 0, -1, -1, 1, 1, -1]
list_direct = [[x,y] for x, y in zip(list_direct_x, list_direct_y)]

# check 0x0 0x1 ... 7x6 7x7
re_input_check = re.compile(r"""^[0-7][0-7]$""")


class Reversi:
    """
    """
    #properties
    inputs = [None, "Black:", "White:"]
    input_method = None
    input_args = None
    suggest = list()
    pass_flag = False
    ui = ""

    def __init__(self):
        self.turns = 0
        self.num_stones = [None, 2, 2]
        self.board = [[EMPTY for _ in range(GRIDS)] for _ in range(GRIDS)]
        self.board[4][3] = 1
        self.board[3][4] = 1
        self.board[3][3] = 2
        self.board[4][4] = 2
        self.player = B # first turn (1:black 2:white)
        self.input_method = input
        self.input_args = self.inputs[self.player]
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
        """ put stone. And check illegal.j
        """
        # check illegal move
        if not self.is_inside(x, y):
            self.message(-1, "x or y is out of range")
            return False
        if not self.is_empty(x, y, self.board):
            self.message(-1, "already stone exists")
            return False
        if not [x, y] in self.suggest:
            self.message(2, f'Error incorrect move: {x},{y}')
            return False
        # put stone
        self.board[x][y] = self.player
        self.kifu.append(str(x)+str(y))
        self.num_stones[self.player] += 1
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
        self.turns += 1
        if self.turns == 61:
            return True
        if self.num_stones[B] == 0:
            return True
        if self.num_stones[W] == 0:
            return True
        if self.pass_flag == 2:
            return True
        return False

    def check_pass(self):
        not_empty__ = [[i, j] for i in range(GRIDS) for j in range(GRIDS) if is_empty(i, j, self.board)]
        for x, y in not_empty__:
            for dx, dy in list_direct:
                if self.check(x, y, dx, dy) != 0:
                    self.board[x][y] = MASK
                    self.suggest.append([x, y])
        return self.suggest

    def clear_suggest(self):
        for x, y in self.suggest:
            if self.board[x][y] == MASK:
                self.board[x][y] = EMPTY
        self.suggest = list()
        return

    def input_move(self):
        """ input stdin. and check string format.
        """
        move = ""
        for _ in range(10):
            try:
                move = self.input_method(self.inputs[self.player])
                if not re_input_check.match(move):
                    self.message(-1, f'Error incorrect input: {move}')
                    continue
                else:
                    break
            except:
                print('Error incorrect input')
                print('Repeat game({})'.format(','.join(self.kifu)))
                exit()
        x, y = [int(i) for i in move]
        return [x, y]

    def win_reason(self):
        s = self.num_stones
        if s[B] == s[W]:
            return "Draw!"
        elif s[B] > s[W]:
            return "Black won!"
        elif s[B] < s[W]:
            return "White won!"

    @staticmethod
    def convert_kifu(ki):
        list_return = list()
        for i in range(0, len(ki), 2):
            list_return.append([CONVERT_DICT[ki[i]], str(int(ki[i+1])-1)])
        return list_return

    def print_score(self):
        print(f"Score[B:{self.num_stones[B]}, W:{self.num_stones[W]}]")
        return

    def score(self):
        return f"Score[B:{self.num_stones[B]}, W:{self.num_stones[W]}]\n"

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
            else:
                return ' x'
        # header
        self.ui = self.score()
        self.ui += '    ' + ' '.join([str(x) for x in range(GRIDS)]) + '\n'
        # board
        for i in range(GRIDS):
            self.ui += str(i) + '0 ' + ''.join(map(rep, self.board[i])) + '\n'
        print(self.ui[:-1])

    def message(self, id=0, message="error message"):
        if id:
            print (f"{message}, Code[{id}]")
        else:
            print (f"{message}")
        pass


# static fucntion
is_inside = Reversi.is_inside
is_empty = Reversi.is_empty
convert_kifu = Reversi.convert_kifu

def game(kifu_input=None):
    ''' start Reversi
    '''
    rv = Reversi()
    # change private function
    put         = rv.put
    flip        = rv.flip
    check       = rv.check
    check_pass  = rv.check_pass
    clr_suggest = rv.clear_suggest
    turn_next   = rv.turn_next
    end         = rv.end
    input_move  = rv.input_move
    output      = rv.output
    msg         = rv.message

    if kifu_input:
        if kifu_input[0] in CONVERT_DICT.keys():
            kifu_input = convert_kifu(kifu_input)
        else:
            kifu_input = [[x[0], x[1]] for x in kifu_input.split(',')]

    # main loop
    while not end():
        if check_pass():
            rv.pass_flag = 0
        else:
            rv.pass_flag += 1
            turn_next()
            continue

        if kifu_input:
            x, y = map(int, kifu_input.pop(0))
        else:
            output()
            x, y = input_move()
        if not put(x, y):
            continue
        clr_suggest()
        # check 8 direction. and turn the stone upside down.
        for dx, dy in list_direct:
            length = check(x, y, dx, dy)
            if length:
                flip(x, y, dx, dy, length)
        turn_next()
    else:
        output()
        msg(0, f"{rv.win_reason()} Final Score Black:{rv.num_stones[B]} White:{rv.num_stones[W]}")
        print('Repeat game(\'{}\')'.format(','.join(rv.kifu)))

def test_game(test=None):
    '''
    >>> game('45,35,22,54,65,56,36,74,76,46,47')
    Score[B:14, W:1]
        0 1 2 3 4 5 6 7
    00  . . . . . . . .
    10  . . . . . . . .
    20  . . ○ . . . . .
    30  . . . ○ ○ ○ ○ .
    40  . . . ○ ○ ○ ○ ○
    50  . . . . ○ . ○ .
    60  . . . . . ○ . .
    70  . . . . ● . ○ .
    Black won! Final Score Black:14 White:1
    Repeat game('45,35,22,54,65,56,36,74,76,46,47')
    >>> game('45,53,42,35,24,55,46,54,64')
    Score[B:13, W:0]
        0 1 2 3 4 5 6 7
    00  . . . . . . . .
    10  . . . . . . . .
    20  . . . . ○ . . .
    30  . . . ○ ○ ○ . .
    40  . . ○ ○ ○ ○ ○ .
    50  . . . ○ ○ ○ . .
    60  . . . . ○ . . .
    70  . . . . . . . .
    Black won! Final Score Black:13 White:0
    Repeat game('45,53,42,35,24,55,46,54,64')
    >>> game('45,35,26,36,46,17,32,53,63,62,61,71,16,15,04,22,12,11,10,00,23,02,01,20,21,51,60,31,30,40,41,03,06,05,13,14,24,25,07,50,27,70,55,37,47,57,67,56,66,76,42,72,54,73,77,65,64,75,74')
    Score[B:26, W:37]
        0 1 2 3 4 5 6 7
    00  ● ○ ● ● ● ● ○ ○
    10  ● ● ● ● ● ○ ○ ○
    20  ● ● ● ● ○ ○ ● ○
    30  ● ● ● ○ ● ● ○ ○
    40  ● ● ● ● ○ ● ○ ○
    50  ● ● . ● ○ ● ○ ○
    60  ● ● ● ● ○ ○ ○ ○
    70  ● ● ● ● ○ ○ ○ ○
    White won! Final Score Black:26 White:37
    Repeat game('45,35,26,36,46,17,32,53,63,62,61,71,16,15,04,22,12,11,10,00,23,02,01,20,21,51,60,31,30,40,41,03,06,05,13,14,24,25,07,50,27,70,55,37,47,57,67,56,66,76,42,72,54,73,77,65,64,75,74')
    >>> game('f5d6c3d3c6f4e3c5f6e6e7f3c4e2f1d1g4g3d7h4h2g5h5h3d2h1g2h6f2b3b4g1a3e1c2c1g6h7h8b1f7f8a5b5a6b6g7g8e8d8c8b8c7a7b7a8b2a1a2a4')
    Score[B:12, W:46]
        0 1 2 3 4 5 6 7
    00  . . ○ . ● ● ● .
    10  ● . ○ ○ ○ ● . ●
    20  ● ● ● ● ● ○ ○ ●
    30  ● ● ● ● ● ○ ○ ●
    40  ● ● ● ● ○ ○ ● ●
    50  ● ● ● ○ ○ ● ● ●
    60  ● ● ● ● ● ● ● ●
    70  ● ● ● ● ● ● ● ●
    White won! Final Score Black:12 White:46
    Repeat game('54,35,22,32,25,53,42,24,55,45,46,52,23,41,50,30,63,62,36,73,71,64,74,72,31,70,61,75,51,12,13,60,02,40,21,20,65,76,77,10,56,57,04,14,05,15,66,67,47,37,27,17,26,06')
    >>> game('f5f6e6f4g5e7f7g6h5d7d6h6h7c6h4c7g4f8d8e8g8h3h2g7c5b6h8c4b3c3c8a3g3g2g1b8a6b7b5b4a8a7a5a4a2b2')
    Score[B:50, W:0]
        0 1 2 3 4 5 6 7
    00  . ○ ○ ○ ○ ○ ○ ○
    10  . ○ ○ ○ ○ ○ ○ ○
    20  . . ○ ○ ○ ○ ○ ○
    30  . . . ○ ○ ○ ○ ○
    40  . . . ○ ○ ○ ○ ○
    50  . . . ○ ○ ○ ○ ○
    60  ○ ○ ○ ○ ○ ○ ○ ○
    70  . ○ ○ ○ ○ ○ ○ ○
    Black won! Final Score Black:50 White:0
    Repeat game('54,55,45,53,64,46,56,65,74,36,35,75,76,25,73,26,63,57,37,47,67,72,71,66,24,15,77,23,12,22,27,02,62,61,60,17,05,16,14,13,07,06,04,03,01,11')
    '''
    pass

if __name__ == '__main__':
        # test exec commandline
        # $ python3 -m doctest reversi.py -v
        game()