import sys
import linecache
import time
import json
import re

import torch


possible_nodes = ['transpose', 'sigmoid']


class Visualizer:
    """
    Base visualization class
    """

    def __init__(self, net):
        self.py_trace = []
        self.torch_trace = []
        self.net = net
        self.regx_op = re.compile(r'\^[a-zA-Z]+')

    def walk_around(self, x):
        sys.settrace(self._global_trace)
        trace, out = torch.jit.trace(self.net, x)
        self._got_tired()
        graph = trace.graph()
        print(graph)
        inputs = list(graph.inputs())
        nodes = list(graph.nodes())
        for node in nodes:
            user = node.uses()[0].user.unique()
            whattype = node.type().scalarType()
            size = node.type().sizes()

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
