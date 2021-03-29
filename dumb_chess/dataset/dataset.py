from typing import List

import numpy as np
import chess.pgn

import requests
import os
import logging
import zipfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DATASET')


class ChessDataset:
    download_url = 'https://www.pgnmentor.com/players/'
    games_dir = './dumb_chess/dataset/games'

    def __init__(self) -> None:
        pass

    def parse_pgn(self):
        result_mapping = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}
        logger.info('Parsing games...')
        listdir = os.litdir(self.games_dir)
        for i, gamef in listdir:
            logger.info(i + 1, '/', len(list_dir))
            with open(os.path.join(self.games_dir, gamef),
                      'r',
                      encoding='utf-8-sig') as game_file:
                games = []
                while True:
                    try:
                        logger.info('Reading game...')
                        game = chess.pgn.read_game(game_file)
                    except UnicodeDecodeError:
                        pass
                    else:
                        if game is None:
                            logger.error('Game is empty')
                        result = game.headers['Result']
                        if result not in result_mapping:
                            logger.error('Game has wrong results...')
                            continue
                        board = game.board()
                        for move in board.first_game.mainline_moves():
                            board.push(move)

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

    def _unzip(self, ffile, dir) -> None:
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

    def __init__(self, board):
        self.board = board

    def serialize(self):
        board_state = np.zeros(64, dtype=np.uint8)
        for i in range(64):
            board_state[i] = self.piece_values[i]
            

if __name__ == '__main__':
    names = ['Adams', 'Hou', 'Adam']
    chessds = ChessDataset()
    chessds._download_games(names)