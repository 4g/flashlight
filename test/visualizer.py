import sys
import linecache
import time
import json

import torch


possible_nodes = {'t': 'transpose', 'addmm': 'addmm', 'sigmoid': 'sigmoid'}


class Visualizer:
    """
    Base visualization class
    """

    def __init__(self, net):
        self.py_trace = []
        self.torch_trace = []
        self.net = net

    @staticmethod
    def _get_user_ids(iterator):
        out = []
        for val in iterator:
            out.append(val.user.unique())
        return out

    @staticmethod
    def _get_node_ids(iterator):
        out = []
        for val in iterator:
            out.append(val.unique())
        return out

    def walk_around(self, x):
        graph = {}
        sys.settrace(self._global_trace)
        trace, out = torch.jit.trace(self.net, x)
        self._got_tired()
        graph_from_tracer = trace.graph()
        # TODO - remove assumption that input is always a single tensor
        model_params = [x] + list(self.net.parameters())
        input_nodes = list(graph_from_tracer.inputs())
        internal_nodes = list(graph_from_tracer.nodes())
        for meta, value in zip(input_nodes, model_params):
            # TODO -  convert display_Values to json serailizable
            graph[meta.unique()] = {
                'display_values': value,
                'display_type': 'tensor',
                'dependancies': [],
                'dependands': self._get_user_ids(meta.uses()),
                'node_name': meta.kind(),
                'datatype': meta.type().scalarType(),
                'shape': meta.type().sizes()}
        for node in internal_nodes:
            graph[node.unique()] = {
                'display_values': None,
                'display_type': None,
                'dependancies': self._get_node_ids(node.inputs()),
                'dependands': self._get_user_ids(node.uses()),
                'node_name': node.kind(),
                'datatype': node.type().scalarType(),
                'shape': node.type().sizes()}

    def _global_trace(self, frame, why, arg):
        if why == 'call':
            code = frame.f_code
            filename = frame.f_globals.get('__file__', None)
            if filename:
                # TODO - check filename always means modulename with value or not
                unwanted = '/home/hhsecond/anaconda3/lib/python3.6/site-packages/'
                if unwanted in filename:
                    filename = filename[53:]
                self.py_trace.append('G==> File: {} -- function: {}'.format(filename, code.co_name))
                return self._local_trace
            else:
                return None

    def _local_trace(self, frame, why, arg):
        if why == "line":
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            unwanted = '/home/hhsecond/anaconda3/lib/python3.6/site-packages/'
            if unwanted in filename:
                filename = filename[53:]
            lineno = frame.f_lineno
            class_obj = frame.f_locals.get("self", None)
            if class_obj is not None:
                class_name = class_obj.__class__.__name__
            else:
                class_name = '<NO_CLASS_NAME>'
            # TODO - remove line, use only line no
            self.py_trace.append(
                "File: {}, class: {}, Line: {} {}".format(
                    filename, class_name, lineno, linecache.getline(filename, lineno)))
        return self._local_trace

    def _got_tired(self):
        sys.settrace(None)
        # TODO - change the filename
        with open('traces/{}.json'.format(time.time()), 'w+') as f:
            json.dump({'py_trace': self.py_trace, 'torch_trace': self.torch_trace}, f, indent=2)
        self.py_trace = []
        self.torch_trace = []
