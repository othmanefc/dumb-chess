from typing import List

import requests
import os
import logging
import zipfile
from tqdm import tqdm

import numpy as np
import chess.pgn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DATASET')


class ChessDataset:
    download_url = 'https://www.pgnmentor.com/players/'
    games_dir = './dumb_chess/dataset/games'

    def __init__(self) -> None:
        pass

    def parse_pgn(self, with_save=False, num_samples=None):
        result_mapping = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}
        logger.info('Parsing games...')
        list_dir = os.listdir(self.games_dir)
        X, y = [], []
        for i, gamef in enumerate(list_dir):
            logger.info(i + 1, '/', len(list_dir))
            with open(os.path.join(self.games_dir, gamef),
                      'r',
                      encoding='utf-8-sig') as game_file:
                while True:
                    try:
                        logger.info('Reading game...')
                        game = chess.pgn.read_game(game_file)
                    except UnicodeDecodeError:
                        pass
                    else:
                        if game is None:
                            logger.error('Game is empty...')
                            break
                        result = game.headers['Result']
                        if result not in result_mapping:
                            logger.error('Game has wrong results...')
                            continue
                        value = result_mapping[result]
                        board = game.board()
                        for move in tqdm(game.mainline_moves(), desc='moves'):
                            board.push(move)
                            serialized = State(board).serialize()
                            X.append(serialized)
                            y.append(value)
                        logger.info(f'serialized {len(X)} examples...')
                        if num_samples and len(X) >= num_samples:
                            logger.info('Number of samples max reached...')
                            break
        self.X, self.y = np.array(X), np.array(y)
        if with_save:
            self.save(len(X))

    def save(self, size) -> None:
        np.savez(
            os.path.join("./dumb_chess/dataset/serialized",
                         f"dataset_{str(size)}.npz"), self.X, self.y)
        logger.info('saved dataset....')

    def load(self, path) -> None:
        data = np.load(path)
        self.X, self.y = data['arr_0'], data['arr_1']

    def _download_games(self, names: List[str]) -> None:
        '''
        Download pgn games for the names
        '''
        for name in names:
            dl_url = self._create_url(name)
            try:
                self._download(dl_url, self.games_dir, name)
            except ValueError:
                continue
            self._unzip(name, self.games_dir)

    def _create_url(self, name: str):
        return self.download_url + name + '.zip'

    def _download(self, url: str, to: str, name: str) -> None:
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            logger.error('Name is not available in the database...')
            raise ValueError
        else:
            open(to + '/' + name + '.zip', 'wb').write(response.content)
            logger.info('Games archive downloaded...')

    def _unzip(self, ffile: str, dir: str) -> None:
        zip_path = dir + '/' + ffile + '.zip'
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dir)
            logger.info('Games archive unzipped...')
        os.remove(zip_path)


class State:
    piece_values = {
        "P": 1,
        "N": 2,
        "B": 3,
        "R": 4,
        "Q": 5,
        "K": 6,
        "p": 9,
        "n": 10,
        "b": 11,
        "r": 12,
        "q": 13,
        "k": 14
    }

    def __init__(self, board: chess.Board = None):
        self.board = board or chess.Board()

    def key(self):
        return (self.board.board_fen(), self.board.turn,
                self.board.castling_rights, self.board.ep_square)

    def serialize(self) -> np.ndarray:
        board_state = np.zeros(64, dtype=np.uint8)
        for i in range(64):
            pp = self.board.piece_at(i)
            if pp:
                board_state[i] = self.piece_values[pp.symbol()]
        self._check_castling_rights(board_state)
        self._check_en_passant(board_state)
        board_state = board_state.reshape(8, 8)

        binary_state = np.zeros((8, 8, 5), dtype=np.uint8)

        binary_state[:, :, 0] = (board_state >> 3) & 1
        binary_state[:, :, 1] = (board_state >> 2) & 1
        binary_state[:, :, 2] = (board_state >> 1) & 1
        binary_state[:, :, 3] = (board_state >> 0) & 1

        binary_state[:, :, 4] = self.board.turn * 1.0

        return binary_state

    def _check_castling_rights(self, board_state: np.ndarray) -> None:
        if self.board.has_queenside_castling_rights(chess.WHITE):
            board_state[0] = 7
        if self.board.has_kingside_castling_rights(chess.WHITE):
            board_state[7] = 7
        if self.board.has_queenside_castling_rights(chess.BLACK):
            board_state[56] = 15
        if self.board.has_kingside_castling_rights(chess.BLACK):
            board_state[63] = 15

    def _check_en_passant(self, board_state: np.ndarray) -> None:
        if self.board.ep_square is not None:
            board_state[self.board.ep_square] = 8

    def possible_moves(self):
        return list(self.board.legal_moves)


if __name__ == '__main__':
    names = ['Adams', 'Hou', 'Adam']
    chessds = ChessDataset()
    chessds._download_games(names)
    chessds.parse_pgn(with_save=True)
