#!/usr/bin/env python3
# coding: utf-8
import traceback

import reversi
from reversi import W,B,GRIDS,CONVERT_DICT,convert_kifu,message,win_reason
import reversi_ai


def game(kifu_input=None):
    ''' start Reversi
    '''
    rv = reversi.Reversi()
    # change private function
    put         = rv.put
    check_pass  = rv.check_pass
    turn_next   = rv.turn_next
    end         = rv.end
    output      = rv.output
    board       = rv.board
    stones      = rv.num_stones


    if kifu_input:
        black_player = reversi.Player(B)
        white_player = reversi.Player(W)
        if kifu_input[0] in CONVERT_DICT.keys():
            kifu_input = convert_kifu(kifu_input)
        else:
            kifu_input = [[int(x[0]), int(x[1])] for x in kifu_input.split(',')]
    else:
        black_player = reversi_ai.AIWrapper(B)
        white_player = reversi_ai.AIPlayer(W)

    # main loop
    while not end():
        if check_pass():
            # pass
            rv.pass_flag += 1
            turn_next()
            continue
        rv.pass_flag = 0

        if kifu_input:
            x, y = kifu_input.pop(0)
            #if not kifu_input:
                #continue
        else:
            #output()
            try:
                if rv.player == B:
                    black_player.input_board(board)
                    x, y = black_player.output_board()
                else:
                    white_player.input_board(board)
                    x, y = white_player.output_board()
            except Exception as e:
                print(e)
                traceback.print_exc()
                exit()
        if put(x, y):
            turn_next()
        else:
            # Error, already exists, irregal put,,,
            continue
    else:
        # Gmae End
        output()
        message(f"{win_reason(stones)} Final Score Black:{stones[B]} White:{stones[W]}")
        print('Repeat game(\'{}\')'.format(','.join(rv.kifu)))

## test ##
def test_game():
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
    >>> game('f5d6c3d3c6f4e3c5f6e6e7f3c4e2f1d1g4g3d7h4h2g5h5h3d2h1g2h6f2b3b4g1a3e1c2c1g6h7h8b1f7f8a5b5a6b6g7g8e8d8c8b8c7a7b7a8b2a1a2a4')
    Score[B:7, W:57]
        0 1 2 3 4 5 6 7
    00  ● ● ● ● ● ● ● ●
    10  ● ● ● ● ● ○ ● ●
    20  ● ● ● ● ● ● ○ ●
    30  ● ● ● ● ● ○ ○ ●
    40  ● ● ● ● ● ○ ● ●
    50  ● ● ● ○ ○ ● ● ●
    60  ● ● ● ● ● ● ● ●
    70  ● ● ● ● ● ● ● ●
    White won! Final Score Black:7 White:57
    Repeat game('54,35,22,32,25,53,42,24,55,45,46,52,23,41,50,30,63,62,36,73,71,64,74,72,31,70,61,75,51,12,13,60,02,40,21,20,65,76,77,10,56,57,04,14,05,15,66,67,47,37,27,17,26,06,16,07,11,00,01,03')
    >>> game('f5f6e6f4g5e7f7g6h5d7d6h6h7c6h4c7g4f8d8e8g8h3h2g7c5b6h8c4b3c3c8a3g3g2g1b8a6b7b5b4a8a7a5a4a2b2')
    Score[B:22, W:18]
        0 1 2 3 4 5 6 7
    00  . . ○ . . . . .
    10  . . ○ ○ . . . .
    20  ● ○ ○ ○ ○ ○ . .
    30  ● ● ○ ○ ○ ○ ○ .
    40  ● ● ● ○ ○ ○ ○ .
    50  ● ● ● ○ ○ ○ . .
    60  ● ● ● ○ ○ . . .
    70  ● ● ● ● ● ● . .
    Black won! Final Score Black:22 White:18
    Repeat game('54,35,22,32,25,53,42,24,55,45,46,52,23,41,50,30,63,62,36,73,71,64,74,72,31,70,61,75,51,12,13,60,02,40,21,20')
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
    >>> game('f5f6e6f4g5e7f7g6h5d7d6h6h7c6h4c7g4f8d8e8g8h3h2g7c5b6h8c4b3c3c8a3g3g2g1b8a6b7b5b4a8a7a5a4a2b2')
    Score[B:7, W:57]
        0 1 2 3 4 5 6 7
    00  ● ● ● ● ● ● ● ●
    10  ● ● ● ● ● ○ ● ●
    20  ● ● ● ● ● ● ○ ●
    30  ● ● ● ● ● ○ ○ ●
    40  ● ● ● ● ● ○ ● ●
    50  ● ● ● ○ ○ ● ● ●
    60  ● ● ● ● ● ● ● ●
    70  ● ● ● ● ● ● ● ●
    White won! Final Score Black:7 White:57
    Repeat game('54,35,22,32,25,53,42,24,55,45,46,52,23,41,50,30,63,62,36,73,71,64,74,72,31,70,61,75,51,12,13,60,02,40,21,20,65,76,77,10,56,57,04,14,05,15,66,67,47,37,27,17,26,06,16,07,11,00,01,03')
    >>> game('f5f6e6f4g5e7f7g6h5d7d6h6h7c6h4c7g4f8d8e8g8h3h2g7c5b6h8c4b3c3c8a3g3g2g1b8a6b7b5b4a8a7a5a4a2b2')
    Score[B:29, W:10]
        0 1 2 3 4 5 6 7
    00  . . ● . . . . .
    10  . . ● . . ● . .
    20  . . ● ● ● ● ● ○
    30  . . . ● ○ ○ ○ ○
    40  . . . ● ○ ○ ○ ○
    50  . . . ○ ○ ○ ○ ○
    60  ○ ○ ○ ○ ○ ○ ○ ○
    70  . ○ ○ ○ ○ ○ ○ ○
    Black won! Final Score Black:29 White:10
    Repeat game('54,55,45,53,64,46,56,65,74,36,35,75,76,25,73,26,63,57,37,47,67,72,71,66,24,15,77,23,12,22,27,02,62,61,60')
    >>> game('54,55,45,53,64,46,56,65,74,36,35,75,76,25,73,26,63,57,37,47,67,72,71,66,24,15,77,23,12,22,27,02,62,61,60,17,05,16,14,13,07,06,04,03,01,11')
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
    >>> game('45,53,62,63,64,25,42,54,55,71,61,51,60,56,46,52,57,70,23,74,75,76,73,50,77,32,16,36,35,13,27,47,03,15,65,26,41,72,40,67,66,14,05,37,12,07,17,01,11,21,31,30,10,04,24,22,20,06,02,00')
    Score[B:32, W:32]
        0 1 2 3 4 5 6 7
    00  ● ● ○ ○ ● ● ● ●
    10  ● ● ○ ○ ● ● ● ○
    20  ● ○ ● ● ○ ○ ● ○
    30  ● ○ ● ○ ○ ○ ● ●
    40  ● ● ○ ○ ○ ○ ○ ●
    50  ● ○ ● ○ ○ ○ ○ ●
    60  ● ● ○ ● ○ ○ ○ ●
    70  ● ● ● ○ ○ ○ ○ ○
    Draw! Final Score Black:32 White:32
    Repeat game('45,53,62,63,64,25,42,54,55,71,61,51,60,56,46,52,57,70,23,74,75,76,73,50,77,32,16,36,35,13,27,47,03,15,65,26,41,72,40,67,66,14,05,37,12,07,17,01,11,21,31,30,10,04,24,22,20,06,02,00')
    >>> message('test',50)
    test code=50
    '''
    pass

if __name__ == '__main__':
        #import doctest
        #doctest.run_docstring_examples(test_game, globals())
        # test exec commandline
        # $ python3 -m doctest reversi.py -v
        game()
        #game('f5f6e6f4g5e7f7g6h5d7d6h6h7c6h4c7g4f8d8e8g8h3h2g7c5b6h8c4b3c3c8a3g3g2g1b8a6b7b5b4a8a7a5a4a2b2')
        #game('54,55,45,53,64,46,56,65,74,36,35,75,76,25,73,26,63,57,37,47,67,72,71,66,24,15,77,23,12,22,27,02,62,61,60')
