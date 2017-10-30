import sys
import linecache
import time
import json
import re

import torch


class Visualizer:
    """
    Base visualization class
    """

    def __init__(self, net):
        self.py_trace = []
        self.torch_trace = []
        self.net = net
        self.regx_op = re.compile(r'\^[a-zA-Z]+')

    def round_a_loop(self, x):
        sys.settrace(self._global_trace)
        trace, out = torch.jit.trace(self.net, x)
        self._terminate_that_loop()
        nodes = trace.graph().nodes()
        for node in nodes:
            val = self.regx_op.search(str(node))
            if val:
                self.torch_trace.append(val.group()[1:])

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
                class_name = ''
            # TODO - remove line, use only line no
            self.py_trace.append(
                "File: {}, class: {}, Line: {} {}".format(
                    filename, class_name, lineno, linecache.getline(filename, lineno)))
        return self._local_trace

    def _terminate_that_loop(self):
        sys.settrace(None)
        # TODO - change the filename
        with open('traces/{}.json'.format(time.time()), 'w+') as f:
            json.dump({'py_trace': self.py_trace, 'torch_trace': self.torch_trace}, f, indent=2)
        print(self.torch_trace)
        self.py_trace = []
        self.torch_trace = []
