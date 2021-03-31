import chess
import tensorflow as tf
import numpy as np

from dumb_chess.dataset.dataset import State


class Valuator:
    MAXVAL = 10_000
    MINVAL = -10_000

    def __init__(self):
        self.model = tf.keras.models.load_model('./model/saved_model')
        self.max, self.min = self.MINVAL, self.MAXVAL
        self.count = 0
        self.memo = {}

    def __call__(self, s: State):
        board = s.serialize()[None].astype(np.float32)
        output = self.model(board)
        return output.numpy()[0]

    def explore_leaves(self, s: State, max_depth=4):
        value, logs = self.compute_min_max(s,
                                           depth=0,
                                           a=self.MINVAL,
                                           b=self.MAXVAL,
                                           max_depth=max_depth,
                                           big=True)
        move = [log[1] for log in logs if log[0] == value][0]
        if s.board.turn:
            print('White moves')
        else:
            print('Black moves')
        print('the move is:', move, value)
        return logs

    def compute_min_max(self, s: State, depth, a, b, max_depth=10, big=False):
        if depth >= max_depth or s.board.is_game_over():
            return self.__call__(s)
        val = self.MINVAL if s.board.turn else self.MAXVAL
        if big:
            log_return = []
        to_sort = []
        for move in s.possible_moves():
            s.board.push(move)
            output = self.__call__(s) * self.get_stoch(depth)
            to_sort.append((move, output))
            s.board.pop()
        moves = sorted(to_sort, key=lambda x: x[1], reverse=s.board.turn)
        if depth > 3:
            moves = moves[:5]

        for move in [x[0] for x in moves]:
            s.board.push(move)
            deep_val = self.compute_min_max(s, depth + 1, a, b, max_depth)
            s.board.pop()
            if big:
                log_return.append((deep_val[0], move))
            if s.board.turn:
                val = max(val, deep_val)
                a = max(a, val)
            elif not s.board.turn:
                val = min(val, deep_val)
                b = min(b, val)
            if a >= b:
                break
        if big:
            return val, log_return
        else:
            return val

    def get_stoch(self, depth):
        param = depth * 0.03
        return np.random.uniform(1 - param, 1 + param)


if __name__ == '__main__':
    s = State()
    v = Valuator()
    a = 0
    moves = []
    while not s.board.is_game_over():
        value, move = v.explore_leaves(s, max_depth=4)
        moves.append(move)
        s.board.push(move)
        a += 1
    print('total moves:', a)
    print(s.board.result())

    with open('./trial.txt', 'w') as f:
        f.truncate(0)
        for item in moves:
            f.write(f'{item}\n')
