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
                row += "0  " if (y, x) in self.__coords else "   "
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
        play = self._check_bad()
        while not play:
            self._draw_hand()
            play = self._check_bad()

    def __repr__(self):
        shape = ""
        for x in range(0, self.__dim):
            row = ""
            for y in range(0, self.__dim):
                row += "0  " if (y, x) in self.__board else "-  "
            shape = row + "\n" + shape
        return shape

    def _check_bad(self):
        for p in self.__hand:
            for x in range(0, self.__dim):
                for y in  range(0, self.__dim):
                    p_playable = True
                    for c in p.get_shape():
                        check_x = x + c[0]
                        check_y = y + c[1]
                        if (check_x, check_y) in self.__board or check_x >= self.__dim or check_y >= self.__dim:
                            p_playable = False
                            break
                    if p_playable:
                        return True
        return False

    def _check_good(self, y_direction=True):
        new_board = []
        check = []
        for x in range(0, self.__dim):
            for y in range(0, self.__dim):
                if (coord := (x, y) if y_direction else (y, x)) in self.__board:
                    check.append(coord)
            if len(check) == self.__dim:
                self.__score += self.__dim
            else:
                new_board += check
            check = []
        return new_board

    def _check_board(self):
        # Check verticals
        b1 = self._check_good(y_direction=True)
        # Check Horizontals
        b2 = self._check_good(y_direction=False)
        new_board = []
        for c in b1:
            if c in b2:
                new_board.append(c)
        self.__board = new_board
        # Check end of game
        self.__play = self._check_bad()

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
        new_coords = []
        for coord in shape:
            play_x = coord[0] + x
            play_y = coord[1] + y
            if (play_x, play_y) in self.__board or play_x >= self.__dim or play_y >= self.__dim:
                print("Invalid Move")
                return
            else:
                new_coords.append((play_x, play_y))
        p_index = self.__hand.index(piece)
        self.__hand = self.__hand[:p_index] + self.__hand[p_index + 1:]
        if self.__hand == list():
            self._draw_hand()
        self.__board += new_coords
        self.__score += len(shape)
        self._check_board()


def main():
    game = Game(dim=10)
    while game.is_playable():
        print(f"Score: {game.get_score()}")
        print(game)
        hand = game.get_hand()
        print_hand = []
        for i in range(0, 3):
            line = ""
            for h2 in hand:
                line += str(h2).split("\n")[i] + "   "
            print_hand.append(line)
        for l in print_hand:
            print(l)
        print("")
        inp = input("p, x, y: ").split(" ")
        try:
            game.play_piece(int(inp[1]), int(inp[2]), hand[int(inp[0])])
        except ValueError or IndexError:
            print("Malformed input")
            continue


if __name__ == "__main__":
    main()
