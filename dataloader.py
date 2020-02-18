import chess.pgn
import os


for file in os.listdir('data'):
    with open(os.path.join('data', file), 'r', encoding="utf-8-sig") as game_file:
            print('file name:', file)
            games = []
            result_mapping = {'1/2-1/2':0, '0-1': -1, '1-0': 1}
            while True:
                try:
                    game = chess.pgn.read_game(game_file)
                except UnicodeDecodeError:
                    pass
                else:
                    if game is None:
                        break
                    result = game.headers['Result']
                    print(dict(game.headers))
