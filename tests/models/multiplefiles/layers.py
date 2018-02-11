from torch import nn
import torch.nn.functional as F


class Layer(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.dense = nn.Linear(input_size, output_size)

    def forward(self, x):
        out = self.dense(x)
        return F.sigmoid(out)
