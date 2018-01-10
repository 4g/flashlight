import torch

from lucent.client.python_tracer import PythonTracer


class FlashLight:
    """ The interface class """
    # TODO - pytorch/onnx version check

    def __init__(self, net):
        self.net = net

    def show_dynamic(self, x):
        """ Slow exploration but captures everything, works only in PyTorch """
        with PythonTracer() as pyt:
            trace, out = torch.jit.trace(self.net, x)
            print(trace)
        for val in trace.graph().nodes():
            print('########################################', val.kind())
            for input_node in val.inputs():
                print(input_node.unique())
            print('>>>>>>>>>>>>>')
            for output in val.outputs():
                print(output)
        for val in pyt.trace:
            pass

    def show_static(self, x):
        """ Fast exploration, wont make dynamic graph, default option for
        graphing from ONNNX
        """
        pass
