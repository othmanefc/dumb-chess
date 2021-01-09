import chess
import numpy as np

piece_map = {
    "p": 0,
    "P": 0,
    "n": 1,
    "N": 1,
    "b": 2,
    "B": 2,
    "r": 3,
    "R": 3,
    "q": 4,
    "Q": 4,
    "k": 5,
    "K": 5
}


class Env:
    def __init__(self, ):
        self.board = chess.Board()
        self.board_space = np.zeros((8, 8, 8))
        self._prev_board_space = None
        self.game_over = False

    def legal_moves(self):
        return list(self.board.legal_moves)

    def save_board_space(self):
        self._prev_board_space = self.board_space.copy()

    def update_board(self):
        self.save_board_space()
        sign = 0
        for i in range(8):
            for j in range(8):
                row, col = i, j
                piece = self.board.piece_at(row * col)
                if not piece:
                    continue
                else:
                    if piece.symbol().isupper():
                        sign = 1
                    else:
                        sign = -1
                position_value = piece_map[piece.symbol()]
                self.board_space[position_value, row, col] = sign
                self.board_space[6, :, :] = 1 / self.board.fullmove_number
                self.board_space[6, 0, :] = 1 if self.board.turn else -1
        self.board_space[7, :, :] = 1

    def _step(self, action):
        current_board_value = self.get_board_value()
        self.board.push(action)
        self.update_board()
        after_board_value = self.get_board_value()
        capture_reward = (after_board_value - current_board_value) * 0.01
        result = self.board.result()
        if result == "*":
            reward = 0
            self.game_over = False
        elif result == "1-0":
            reward = 1
            self.game_over = True
        elif result == "0-1":
            reward = -1
            self.game_over = True
        elif result == "1/2-1/2":
            reward = 0
            self.game_over = True
        else:
            raise ValueError("result value is not valid ")
        reward += capture_reward
        return reward

    def get_board_value(self):
        value = 0
        piece_values = {"p": 1, "r": 5, "b": 3, "n": 3, "q": 9, "k": 0}
        for pp, val in piece_values.items():
            value += val * np.sum(self.board_space[piece_map[pp], :, :])
        return value
    
    def random_action(self):
        return np.random.choice(self.legal_moves())

