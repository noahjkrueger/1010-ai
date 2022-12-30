import argparse

from EscapeColors import EscapeColors
from Game1010 import Game
from sys import argv


def main(args):
    parser = argparse.ArgumentParser(
        prog="python3 1010-ai.py",
        description="AI that gets max score in the 1010! game",
        prefix_chars="--",
    )
    p_args = parser.parse_args(args)
    game = Game()
    while True:
        print(game.get_score(), "\n", game)
        hand = game.get_hand()
        for h in hand:
            print(h)
        inp = input("p, x, y: ").split(" ")
        game.play_piece(int(inp[1]), int(inp[2]), hand[int(inp[0])])


if __name__ == "__main__":
    main(argv[1:])
