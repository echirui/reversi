import reversi
from reversi import W,B,EMPTY,GRIDS,CONVERT_DICT,convert_kifu,list_direct,re_input_check,MASK
from copy import copy
from sys import stderr


pointmap = [[8,7,6,6,6,6,7,8],
            [7,7,5,5,5,5,7,7],
            [6,5,4,4,4,4,5,6],
            [6,5,4,3,3,4,5,6],
            [6,5,4,3,3,4,5,6],
            [6,5,4,4,4,4,5,6],
            [7,7,5,5,5,5,7,7],
            [8,7,6,6,6,6,7,8]]
class AI(reversi.Player):
    rv = None
    def __init__(self, color, board=None):
        self.rv = reversi.Reversi()
        super().__init__(color)

    def input_board(self, board):
        self.rv.board = board
        self.rv.player = self.color
        return super().input_board(board)

    def output_board(self):
        self.rv.clear_suggest()
        self.rv.check_pass()
        if sum(count(self.rv, self.rv.player)) == 4:
            return 4,5
        suggest = copy(self.rv.suggest)
        ret_x, ret_y = '', ''
        max_suggest = -9999
        for x, y in suggest:
            my_rv = copy(self.rv)
            my_rv.put(x, y)
            for dx, dy in list_direct:
                length = my_rv.check(x, y, dx, dy)
                if length:
                    my_rv.flip(x, y, dx, dy, length)
            my_rv.turn_next()
            my_rv.check_pass()
            #l = len(my_rv.suggest)
            #my_stones, opponet_stones = count(my_rv, self.color)
            #point = l * (((64 - opponet_stones)/ 64) + (my_stones / 64))
            #point = l * evaluation(my_rv)
            point = evaluation(self.rv.player, my_rv, 2)
            #print(max_suggest, point, ret_x,ret_y,x,y, file=stderr)
            if point > max_suggest:
                max_suggest = point
                ret_x, ret_y = x, y
            my_rv = None
        if self.rv.suggest:
            self.rv.suggest = None
        return ret_x, ret_y

def evaluation(player, rv: reversi.Reversi, depth=0):
    p = [-1.0, 1.0, -12.0, 1, -1]
    output = list()
    suggests = len(rv.suggest)
    max_eval_point = -9999
    my_stones, opponet_stones, my_point, opponet_point = count(rv, rv.player)
    if my_stones >= 40:
        my_stones = 300
    elif my_stones >= 32:
        my_stones = 32
    else:
        my_stones = 0
    output = [opponet_point,my_point,suggests,my_stones,opponet_stones],p
    output = [x*y for x,y in zip([opponet_point,my_point,suggests,my_stones,opponet_stones],p)]
    s = sum(output)
    #print(output,s,depth, file=stderr)
    return s

def count(rv: reversi.Reversi, color):
    my_stones = 0
    opponet_stones = 0
    my_point = 0
    opponet_point = 0
    for i, line in enumerate(rv.board):
        for j, grid in enumerate(line):
            if rv.player == grid:
                opponet_stones += 1
                opponet_point += pointmap[i][j]
            if rv.player^MASK == grid:
                my_stones += 1
                my_point += pointmap[i][j]
    return my_stones, opponet_stones, my_point, opponet_point

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