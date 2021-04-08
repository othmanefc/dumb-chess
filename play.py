import logging
from flask import Flask, request

import chess

from dumb_chess.dataset import State
from dumb_chess.search_tree import Valuator

logger = logging.getLogger('game')
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

s = State()
v = Valuator()


def computer_move(s: State, v: Valuator) -> None:
    move = sorted(v.explore_leaves(s),
                  key=lambda x: x[0],
                  reverse=s.board.turn)
    if not move:
        return
    for i, m in enumerate(move[:3]):
        logger.info(f'top {i +1} move: {m}')
    color = 'white' if s.board.turn else 'black'
    logger.info(f'{color} moving {move[0][1]}')
    s.board.push(move[0][1])


@app.route('/')
def hello_world():
    page = open("index.html").read()
    return page.replace('start', s.board.fen())


@app.route('/move')
def move():
    if not s.board.is_game_over():
        source = int(request.args.get('from', default=''))
        target = int(request.args.get('to', default=''))
        promotion = True if request.args.get('promotion',
                                             default='') == 'true' else False
        move = s.board.san(
            chess.Move(source,
                       target,
                       promotion=chess.QUEEN if promotion else None))
        if move:
            logger.info(f'Human moves {move}')
            try:
                s.board.push_san(move)
            except Exception:
                response = app.response_class(response='illegal move',
                                              status=200)
                return response
            logger.info('Waiting for computer moves...')
            computer_move(s, v)
            response = app.response_class(response=s.board.fen(), status=200)
            return response
    else:
        results = {'1-2/1-2': 'Draw', '1': 'White wins', '-1': 'Black wins'}
        response = app.response_class(response=results[s.board.result()],
                                      status=200)
        return response


@app.route('/newgame')
def newgame():
    s.board.reset()
    logger.info('Board reset...')
    response = app.response_class(response=s.board.fen(), status=200)
    return response


@app.route("/undo")
def undo():
    # s.board.pop()
    response = app.response_class(response=s.board.fen(), status=200)
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
