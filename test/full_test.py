import torch
from torch import nn
from torch.autograd import Variable
from flashlight import FlashLight

from models.multiplefiles import multimain
from models.singlefile import singlemain


class TestDirectTorchLayers:

    def test_sequential(self):
        net = nn.Sequential(nn.Linear(3, 2), nn.Linear(2, 1))
        fl = FlashLight(net)
        dummydata = Variable(torch.FloatTensor(1, 3))
        assert fl.show_dynamic(dummydata) is None


class TestSingleModelFile:

    def test_single_class(self):
        net = singlemain.singleNet(10, 5, 4)
        fl = FlashLight(net)
        dummydata = Variable(torch.FloatTensor(1, 10))
        assert fl.show_dynamic(dummydata) is None

    def test_multiple_classes(self):
        net = singlemain.MultiNetParent(10, 5, 4)
        fl = FlashLight(net)
        dummydata = Variable(torch.FloatTensor(1, 10))
        assert fl.show_dynamic(dummydata) is None


class TestMultipleModelFiles:

    def test_two_classes(self):
        net = multimain.Network(10, 5, 4)
        fl = FlashLight(net)
        dummydata = Variable(torch.FloatTensor(1, 10))
        assert fl.show_dynamic(dummydata) is None
