from torch import nn
from models.multiplefiles.layers import Layer

input_size = 10


class Network(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # A simple heuristic to find the hiddenlayer size
        self.fc1 = Layer(input_size, hidden_size)
        self.fc2 = Layer(hidden_size, output_size)

    def forward(self, batch):
        l1 = self.fc1(batch)
        l2 = self.fc2(l1)
        return l2
