#!/usr/bin/env python3
# coding: utf-8

import re
import sys

GRIDS = 8
EMPTY = 0    # 2bit 0b00
B = 1    # 2bit 0b01
W = 2    # 2bit 0b10
MASK = 0b11 # and enable flag 2bit 0b11

# R, D, L, U, RU, RD, LD, LU
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
        self.next = B # first turn (1:black 2:white)
        self.input_method = input
        self.input_args = self.inputs[self.next]
        self.kifu = list()

    @staticmethod
    def is_inside(x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def is_empty(self, x, y):
        return not (self.board[x][y] == B or self.board[x][y] == W)

    def check(self, x, y, dx, dy):
        length = 0
        for i in range(1, GRIDS):
            nx = x + i*dx
            ny = y + i*dy
            if not self.is_inside(nx, ny):
                return 0
            if self.is_empty(nx, ny):
                return 0
            if self.board[nx][ny] != self.next:
                length += 1
            elif self.board[nx][ny] == self.next:
                return length

    def flip(self, x, y, dx, dy, length):
        for i in range(1,length+1):
            self.swap(x+dx*i,y+dy*i)
        return

    def swap(self, x, y):
        self.num_stones[self.next] += 1
        self.num_stones[self.next^MASK] -= 1
        self.board[x][y] = self.board[x][y] ^ MASK
        return

    def put(self, x, y):
        """ put stone. And check illegal
        """
        # check illegal move
        if not self.is_inside(x, y):
            self.message(-1, "x or y is out of range")
            return False
        if not self.is_empty(x, y):
            self.message(-1, "already stone exists")
            return False
        if not [x, y] in self.suggest:
            self.message(2, f'Error incorrect move: {x},{y}')
            return False
        # put stone
        self.board[x][y] = self.next
        self.num_stones[self.next] += 1
        return True
    
    def next_turn(self):
        """
        """
        # 01 xor 11 = 10, 10 xor 11 = 01
        self.next = self.next ^ MASK
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
        not_empty__ = [[i, j] for i in range(GRIDS) for j in range(GRIDS) if self.is_empty(i, j)]
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
                move = self.input_method(self.inputs[self.next])
                if not re_input_check.match(move):
                    self.message(-1, f'Error incorrect input: {move}')
                    continue
                else:
                    break
            except:
                print('Error incorrect input')
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
        #print('    ' + ' '.join([str(x) for x in range(GRIDS)]))
        # board
        for i in range(GRIDS):
            self.ui += str(i) + '0 ' + ''.join(map(rep, self.board[i])) + '\n'
            #print(str(i) + '0 ' + ''.join(map(rep, self.board[i])))
        print(self.ui[:-1])

    def message(self, id=0, message="error message"):
        if id:
            print (f"{message}, Code[{id}]")
        else:
            print (f"{message}")
    
        pass
    
def game(test_input=None):
    ''' start Reversi
    '''
    rv = Reversi()
    # change private function
    put         = rv.put
    flip        = rv.flip
    check       = rv.check
    check_pass  = rv.check_pass
    clr_suggest = rv.clear_suggest
    next_turn   = rv.next_turn
    end         = rv.end
    input_move  = rv.input_move
    output      = rv.output
    msg         = rv.message

    pre_input = None
    if test_input:
        pre_input = test_input.split(',')
        pre_input = [[x[0], x[1]] for x in pre_input]
    
    # main loop
    while not end():
        if check_pass():
            rv.pass_flag = 0
        else:
            rv.pass_flag += 1
            next_turn()
            continue

        if pre_input:
            x, y = map(int, pre_input.pop(0))
        else:
            output()
            x, y = input_move()
        if not put(x, y):
            continue
        rv.kifu.append((x,y,))
        clr_suggest()
        # check 8 direction. and turn stone up side down.
        for dx, dy in list_direct:
            length = check(x, y, dx, dy)
            if length:
                flip(x, y, dx, dy, length)
        next_turn()
    else:
        output()
        msg(0, f"{rv.win_reason()} Final Score Black:{rv.num_stones[B]} White:{rv.num_stones[W]}")
        #print(rv.kifu)

def test_game(test=None):
    '''
    >>> game('45,35,22,54,65,56,36,74,76,46,47,55')
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
    '''
    '''
    >>> game('45,35,26,36,46,17,32,53,63,62,61,71,16,15,04,22,12,11,10,00,23,02,01,20,21,51,60,31,30,40,41,03,06,05,13,14,24,25,07,50,27,70,55,37,47,57,67,77,56,66,76,73,42,72,54')
    Score[B:28, W:31]
        0 1 2 3 4 5 6 7
    00  ● ○ ● ● ● ● ○ ○
    10  ● ● ● ● ● ○ ○ ○
    20  ● ● ● ● ○ ○ ○ ○
    30  ● ○ ● ○ ○ ● ○ ○
    40  ● ● ○ ○ ○ ○ ○ ○
    50  ● ● . ● ○ ○ ○ ○
    60  ● ● ● ● . . ○ ○
    70  ● ● ● ● . . ○ ●
    White won! Final Score Black:28 White:31
    '''
    pass
        
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        import doctest
        doctest.run_docstring_examples(test_game, globals())
    else:
        game()
