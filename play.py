from flask import Flask, Response, request
from termcolor import colored

from colorama import Style, Back, Fore
import numpy as np
import pandas as pd

from dumb_chess.dataset import State
from dumb_chess.search_tree import Valuator

# app = Flask(__name__)
s = State()
v = Valuator()


def computer_move(s: State, v: Valuator):
    try:
        moves = sorted(v.explore_leaves(s),
                       key=lambda x: x[0],
                       reverse=s.board.turn)
    except Exception:
        moves = []

    if len(moves) == 0:
        m1 = "game over"
        return m1
    print(colored(Style.BRIGHT + "top 3:", 'green'))

    for i, m in enumerate(moves[:3]):
        mi = str(m)
        m1 = mi.split('(', )[1]
        m2 = m1.split(",", )[0]
        m = mi.split("'", )[1]
        print("  ", colored(Style.DIM + "Value increase: ", 'green'),
              colored(Style.BRIGHT + m2, 'cyan'),
              colored(Style.DIM + " for move ", 'green'),
              colored(Style.BRIGHT + m, 'cyan'))
        if not s.board.turn:
            comp = colored(Back.WHITE + Fore.BLACK + Style.DIM + "Agent-K")
        else:
            comp = colored(Back.MAGENTA + Fore.CYAN + Style.BRIGHT + "Agent-J")
    print(comp, colored(Style.BRIGHT + "moving", 'magenta'),
          colored(Style.BRIGHT + str(moves[0][1]), 'yellow'))


# @app.route('/')
# def hello_world():
#     page = open("index.html").read()
#     return page.replace('start', s.board_fen())

if __name__ == '__main__':
    computer_move(s, v)