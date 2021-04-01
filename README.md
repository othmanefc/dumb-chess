## DUMB CHESS AI

A dumb chess project, training an evulation function on several games from top GrandMaster players. This is nor AlphaZero or DeepBlue, just a simple MinMax model with AlphaBeta pruning, using a Neural Network as an evaluation function

### How It Works

#### Evaluation Function
The evaluation function, as said above is a Neural network that is fed serialized chessboards as 5x8x8 array coded as bytes (see BitBoard). The Function doesn't look in the future and simple 1 after.

#### MinMax
Next we’re going to create a search tree from which the algorithm can chose the best move. This is done by using the Minimax algorithm.

In this algorithm, the recursive tree of all possible moves is explored to a given depth, and the position is evaluated at the ending “leaves” of the tree.

After that, we return either the smallest or the largest value of the child to the parent node, depending on whether it’s a white or black to move. (That is, we try to either minimize or maximize the outcome at each level.)

### How to use it 
The repositories already comes with a trained model, that you can directly use with the GUI. However, if you want to train, your own model, you need first to download game files. You can do that with `download.py`, it will also serialize the dataset for training and store it:

``` bash
python3 download.py --names Kasparov Adams Capablanca
```
Replace the names I've put with the ones you want, you can put as much as you like as long as they are available in the pgnmentor.com website.

You can then train the model with specifying some paramaters:

`dataset` : name of the *.npz file that should be located on /dumb_ches/dataset/serialized.
`epochs`  : (default to 10) Epochs.
`bs`: (default to 16) Batch size.

```bash
python3 train.py
```

Afterward, when the training is over, you can simply run the flask app with:
``` bash
python3 play.py
```
