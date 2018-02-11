from torch import nn
import torch.nn.functional as F

input_size = 10


class singleNet(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # A simple heuristic to find the hiddenlayer size
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, batch):
        l1 = self.fc1(batch)
        act = F.sigmoid(l1)
        l2 = self.fc2(act)
        return F.tanh(l2)


class MultiNetParent(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # A simple heuristic to find the hiddenlayer size
        self.fc1 = MultipleNetChild(input_size, hidden_size)
        self.fc2 = MultipleNetChild(hidden_size, output_size)

    def forward(self, batch):
        out = self.fc1(batch)
        return self.fc2(out)


class MultipleNetChild(nn.Module):

    def __init__(self, input_size, output_size):
        super().__init__()
        # A simple heuristic to find the hiddenlayer size
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, batch):
        l1 = self.fc(batch)
        return F.sigmoid(l1)
