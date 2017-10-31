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

    def walk_around(self, x):
        sys.settrace(self._global_trace)
        trace, out = torch.jit.trace(self.net, x)
        self._got_tired()
        graph = trace.graph()
        inputs = list(graph.inputs())
        nodes = list(graph.nodes())
        # print(inputs)
        # print(nodes)
        # exit()

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

    def _got_tired(self):
        sys.settrace(None)
        # TODO - change the filename
        with open('traces/{}.json'.format(time.time()), 'w+') as f:
            json.dump({'py_trace': self.py_trace, 'torch_trace': self.torch_trace}, f, indent=2)
        print(self.torch_trace)
        self.py_trace = []
        self.torch_trace = []

"""
graph(%1 : Float(64, 10)
      %2 : Float(100, 10)
      %3 : Float(100)
      %4 : Float(4, 100)
      %5 : Float(4)) {
  %7 : Float(10!, 100!) = ^Transpose(0, 1)(%2), uses = [[%8.i2]];
  %9 : Float(64, 100), %10 : Handle = ^Addmm(1, 1, False)(%3, %1, %7), uses = [[%11.i0], []];
  %12 : Float(64, 100) = ^Sigmoid()(%9), uses = [[%15.i1]];
  %14 : Float(100!, 4!) = ^Transpose(0, 1)(%4), uses = [[%15.i2]];
  %16 : Float(64, 4), %17 : Handle = ^Addmm(1, 1, False)(%5, %12, %14), uses = [[%18.i0], []];
  %19 : Float(64, 4) = ^Sigmoid()(%16), uses = [[%0.i0]];
  return (%19);
}


[%1 : Float(64, 10) = Param(), uses = [%8.i1];
, %2 : Float(100, 10) = Param(), uses = [%6.i0];
, %3 : Float(100) = Param(), uses = [%8.i0];
, %4 : Float(4, 100) = Param(), uses = [%13.i0];
, %5 : Float(4) = Param(), uses = [%15.i0];
]
"""