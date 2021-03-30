import argparse
import logging

from dumb_chess.dataset import ChessDataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DOWNLOAD')

parser = argparse.ArgumentParser()
parser.add_argument(
    '-p',
    '--players',
    action='store',
    nargs='+',
    required=True,
    type=str,
)
args = parser.parse_args()
data = ChessDataset()


def main():
    for name in args.players:
        logger.info(f"Downloading games for {name}...")
    try:
        data._download_games(args.players)
    except Exception:
        logger.error('could not download the games, will try to parse what is in memory')
    logger.info('Started parsing the games...')
    data.parse_pgn(with_save=True)
    logger.info('Ended parsing')


if __name__ == '__main__':
    main()
