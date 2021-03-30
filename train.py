import os
import argparse

import tensorflow as tf
import numpy as np

from dumb_chess.model import Net
from dumb_chess.dataset import ChessDataset

PATH = os.path.join('dumb_chess', 'dataset', 'serialized',
                    'dataset_444920.npz')
parser = argparse.ArgumentParser()

parser.add_argument(
    "--dataset",
    type=str,
    default='dataset_444920.npz',
    help=
    'name of dataset which should be located on /dumb_chess/dataset/serialized'
)
parser.add_argument("--epochs", type=int, default=10)
parser.add_arguement("--bs", type=int, default=16)

args = parser.parse_args()

data = ChessDataset()
data.load(PATH)

X, y = data.X, data.y
X = X.astype(np.float32)
X = np.moveaxis(X, 1, -1)  # Channels last
print(X.shape, y.shape)


def main():
    model = Net()
    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  optimizer=tf.keras.optimizers.Adam())
    model.build((None, 8, 8, 5))
    print(model.summary())
    model.fit(X, y, batch_size=args.bs, epochs=args.epochs, verbose=True)


if __name__ == '__main__':
    main()