import reversi
from reversi import W,B,EMPTY,GRIDS,CONVERT_DICT,convert_kifu,list_direct,re_input_check
import random
from copy import copy

class AI(reversi.Player):
    rv = None
    def __init__(self, color, board=None):
        self.rv = reversi.Reversi()
        self.rv.board = board
        super().__init__(color)

    def input_board(self, board):
        self.rv = reversi.Reversi(copy(board))
        self.rv.player = self.color
        return super().input_board(board)

    def output_board(self):
        self.rv.clear_suggest()
        self.rv.check_pass()
        suggest = copy(self.rv.suggest)
        ret_x, ret_y = '', ''
        min_suggest = 999
        for x, y in suggest:
            my_rv = copy(self.rv)
            my_rv.put(x, y)
            for dx, dy in list_direct:
                length = my_rv.check(x, y, dx, dy)
                if length:
                    my_rv.flip(x, y, dx, dy, length)
            my_rv.turn_next()
            my_rv.check_pass()
            l = len(my_rv.suggest)
            opponet_stones = 0
            my_stones = 0
            for line in my_rv.board:
                for grid in line:
                    if my_rv.player == grid:
                        opponet_stones += 1
                    if self.rv.player == grid:
                        my_stones += 1
            point = l * (((64 - opponet_stones)/ 64) + (my_stones / 64))
            #print(min_suggest, l, my_stones, opponet_stones, ret_x,ret_y,x,y)
            if point < min_suggest:
                min_suggest = point
                ret_x, ret_y = x, y
            my_rv = None
        if self.rv.suggest:
            self.rv.suggest = None
        return ret_x, ret_y

def main():
    while True:
        player = int(input())
        grid = [[int(i) for i in input().split()] for _ in range(GRIDS)]
        ai = AI(player, grid)
        ai.input_board(grid)
        x, y = ai.output_board()
        print(f'{x} {y}')

if __name__ == "__main__":
    main()