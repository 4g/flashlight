import json

import torch
from torch.autograd import Variable
from torch import nn
import torch.nn.functional as F
import torch.optim as optim

from visualizer import Visualizer


class GameInfo:

    def __init__(self, batch_size):
        self.batch_size = batch_size
        processed_game_input = []
        processed_game_output = []
        teams = set()
        grounds = set()
        with open('formatteddata.json', 'r') as f:
            for game in json.load(f):
                game[6] = int(game[6].lower() == 'bat')
                teams.add(game[2])
                teams.add(game[3])
                grounds.add(game[4])
                # adding relevent info
                processed_game_input.append([game[2], game[3], game[5], game[4], game[6]])
                processed_game_output.append(int(game[7] == game[3]))

        self.inputs = processed_game_input
        self.outputs = processed_game_output
        self.team_to_idx = {v: k for k, v in enumerate(teams)}
        self.idx_to_team = {v: k for v, k in self.team_to_idx.items()}
        self.ground_to_idx = {v: k for k, v in enumerate(grounds)}
        self.idx_to_ground = {v: k for v, k in self.ground_to_idx.items()}

        for game in self.inputs:
            game[0] = self.team_to_idx[game[0]]
            game[1] = self.team_to_idx[game[1]]
            game[2] = self.team_to_idx[game[2]]
            game[3] = self.ground_to_idx[game[3]]
        self.inputs = Variable(torch.LongTensor(self.inputs), requires_grad=False)
        self.outputs = Variable(torch.LongTensor(self.outputs))
        self.augment_data()
        self.data_length = len(self.inputs[1])

    def augment_data(self):
        pass

    def training_set(self):
        no_of_batches = int(len(self.inputs) / self.batch_size)
        training_set_in = self.inputs[:int(len(self.inputs) * 0.9)]
        training_set_out = self.outputs[:int(len(self.inputs) * 0.9)]
        for batch in range(no_of_batches):
            start = batch * self.batch_size
            end = start + self.batch_size
            yield (training_set_in[start:end], training_set_out[start:end])

    def testing_set(self):
        return self.inputs[int(len(self.inputs) * 0.9):], self.outputs[int(len(self.inputs) * 0.9):]


class CricketNet(nn.Module):
    def __init__(self, team_count, ground_count):
        super().__init__()
        team_embed_size = 2
        ground_embed_size = 2
        toss_embed_size = 1
        hidden_size = 20
        self.team_embedder = nn.Embedding(team_count, team_embed_size)
        self.ground_embedder = nn.Embedding(ground_count, ground_embed_size)
        self.toss_embedder = nn.Embedding(2, toss_embed_size)
        input_size = (team_embed_size * 3) + ground_embed_size + toss_embed_size
        self.dropout = nn.Dropout(p=0.5)
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 2)

    def forward(self, batch):
        team1 = self.team_embedder(batch[:, 0])
        team2 = self.team_embedder(batch[:, 1])
        toss_winner = self.team_embedder(batch[:, 2])
        host = self.ground_embedder(batch[:, 3])
        toss_decision = self.toss_embedder(batch[:, 4])
        inputs = torch.cat((team1, team2, toss_winner, host, toss_decision), dim=1)
        inputs = self.dropout(inputs)
        a = F.selu(self.fc1(inputs))
        b = self.fc2(a)
        log_probs = F.log_softmax(b)
        return log_probs


lr = 0.01
batch_size = 200
epochs = 100

games = GameInfo(batch_size)
net = CricketNet(len(games.team_to_idx), len(games.ground_to_idx))
viz = Visualizer(net)
loss_function = nn.NLLLoss()
optimizer = optim.Adam(net.parameters(), lr=lr)
total_loss = []
for epoch in range(epochs):
    for batch in games.training_set():
        net.zero_grad()
        log_prob = net(batch[0])
        loss = loss_function(log_prob, batch[1])
        loss.backward()
        optimizer.step()
    total_loss.append(loss.data[0])
    if not epoch % 50:
        print(loss.data[0], epoch)
        viz.walk_around(batch[0])

# add volatile option
testing_set = games.testing_set()
log_prob = net(testing_set[0])
print('test result')
print((log_prob.max(1)[1] == testing_set[1]).sum().data[0] / len(testing_set[1]))
