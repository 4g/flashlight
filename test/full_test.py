import torch
from torch import nn
from torch.autograd import Variable
from lucent import Lucent


class TestClass:

    def test_first(self):
        net = nn.Sequential(nn.Linear(3, 2), nn.Linear(2, 1))
        lucent_torch = Lucent(net)
        dummydata = Variable(torch.FloatTensor(1, 3))
        assert lucent_torch.show_dynamic(dummydata) is None
