from random import randint
from EscapeColors import EscapeColors


class _Piece:
    def __init__(self, shape_string):
        self.__ss = shape_string
        if len(shape_string) > 9:
            raise Exception(f"{EscapeColors.BOLD}{EscapeColors.FAIL}FAIL:{EscapeColors.ENDC}"
                            f" '{shape_string}' is longer than 9")
        self.__coords = []
        x = 0
        y = 2
        for s in shape_string:
            if s == "1":
                self.__coords.append((x, y))
            if x == 2:
                y -= 1
                x = 0
            else:
                x += 1

    def __repr__(self):
        shape = ""
        for x in range(0, 3):
            row = ""
            for y in range(0, 3):
                row += "O  " if (y, x) in self.__coords else "-  "
            shape = row + "\n" + shape
        return shape

    def get_shape(self):
        return self.__coords


class Game:
    def __init__(self, dim=10):
        self.__dim = dim
        self.__score = 0
        self.__board = []
        self.__hand = []
        self.__play = True

        self.__pieces = []

        self.__pieces.append(_Piece("000000100"))  # 1x1
        self.__pieces.append(_Piece("000110110"))  # 2x2
        self.__pieces.append(_Piece("111111111"))  # 3x3
        self.__pieces.append(_Piece("000000111"))  # 3x1
        self.__pieces.append(_Piece("100100100"))  # 1x3
        self.__pieces.append(_Piece("000000110"))  # 2x1
        self.__pieces.append(_Piece("000100100"))  # 1x2
        self.__pieces.append(_Piece("111100100"))  # big L -+ apex
        self.__pieces.append(_Piece("111001001"))  # big L ++ apex
        self.__pieces.append(_Piece("001001111"))  # big L +- apex
        self.__pieces.append(_Piece("100100111"))  # big L -- apex
        self.__pieces.append(_Piece("000110100"))  # small L -+ apex
        self.__pieces.append(_Piece("000110010"))  # small L ++ apex
        self.__pieces.append(_Piece("000010110"))  # small L +- apex
        self.__pieces.append(_Piece("000100110"))  # small L -- apex
        self._draw_hand()

    def __repr__(self):
        shape = ""
        for x in range(0, self.__dim):
            row = ""
            for y in range(0, self.__dim):
                row += "O  " if (y, x) in self.__board else "-  "
            shape = row + "\n" + shape
        return shape

    def _check_bad(self): #TODO -------------------------------
        playable = False
        for shape in self.__hand:
            for x in range(0, self.__dim):
                for y in range(0, self.__dim):
                    for coord in shape:
                        check_x = x + coord[0]
                        check_y = y + coord[1]
                        if (check_x, check_y) in self.__board:
                            break
        self.__play = playable

    def _check_good(self, y_direction=True):
        new_board = []
        check = []
        for x in range(0, self.__dim):
            for y in range(0, self.__dim):
                if (coord := (x, y) if y_direction else (y, x)) in self.__board:
                    check.append(coord)
            if len(check) == 10:
                self.__score += 10
            else:
                new_board += check
            check = []
        self.__board = new_board

    def _check_board(self):
        # Check verticals
        self._check_good(y_direction=True)
        # Check Horizontals
        self._check_good(y_direction=False)
        # Check end of game
        #self._check_bad()

    def _draw_hand(self):
        self.__hand = [self.__pieces[randint(0, len(self.__pieces) - 1)] for i in range(0, 3)]

    def get_hand(self):
        return self.__hand

    def get_score(self):
        return self.__score

    def is_playable(self):
        return self.__play

    def play_piece(self, x, y, piece):
        shape = piece.get_shape()
        new_board = self.__board
        for coord in shape:
            play_x = coord[0] + x
            play_y = coord[1] + y
            if (play_x, play_y) in self.__board:
                print("Invalid Move")
                return
            else:
                new_board.append((play_x, play_y))
        p_index = self.__hand.index(piece)
        self.__hand = self.__hand[:p_index] + self.__hand[p_index + 1:]
        if self.__hand == list():
            self._draw_hand()
        self.__board = new_board
        self.__score += len(shape)
        self._check_board()

