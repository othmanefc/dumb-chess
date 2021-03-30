from torch.utils.data import Dataset
from.dataset import ChessDataset

class TorchDataset(Dataset):
    def __init__(self, path):
        data = np.load(path)
        self.X, self.y = data['arr_0'], data['arr_1']

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
