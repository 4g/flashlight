import sys
import linecache
import time
import json

import torch

# addInput
# advanceStage
# appendNode
# at
# create
# createClone
# createConstant
# createFusionGroup
# createSelect
# eraseInput
# inputs
# lint
# nodes
# op
# outputs
# prependNode
# registerOutput
# stage


# addInput
# attributeNames
# cconv
# copyAttributes
# debugName
# destroy
# f
# f_
# fs
# fs_
# g
# g_
# gs
# gs_
# hasAttribute
# hasAttributes
# hasMultipleOutputs
# hasType
# i
# i_
# inferTypeFrom
# input
# inputs
# insertAfter
# insertBefore
# is
# is_
# kind
# kindOf
# moveAfter
# moveBefore
# offset
# outputs
# pyname
# pyobj
# removeAllInputs
# removeAttribute
# removeInput
# replaceAllUsesWith
# replaceInput
# replaceInputWith
# s
# s_
# scalar_args
# setDebugName
# setStage
# setType
# ss
# ss_
# stage
# t
# t_
# ts
# ts_
# type
# typeAs
# typeOption
# unique
# uniqueName
# uses']

class Visualizer:
    """
    Base visualization class
    """

    def __init__(self, net):
        self.py_trace = []
        self.net = net

    def round_a_loop(self, x):
        sys.settrace(self._global_trace)
        trace, out = torch.jit.trace(self.net, x)
        self._terminate_the_loop()
        self.torch_trace = str(trace)
        nodes = trace.graph().nodes()
        for node in nodes:
            print(node.is_())
        exit()

    def _global_trace(self, frame, why, arg):
        if why == 'call':
            code = frame.f_code
            filename = frame.f_globals.get('__file__', None)
            if filename:
                # TODO - check filename always means modulename with value or not
                self.py_trace.append({'global': [filename, code.co_name], 'local': []})
                return self._local_trace
            else:
                return None

    def _local_trace(self, frame, why, arg):
        if why == "line":
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            # TODO - remove line, use only line no
            self.py_trace[-1]['local'].append(
                [filename, lineno, linecache.getline(filename, lineno)])
        return self._local_trace

    def _terminate_the_loop(self):
        sys.settrace(None)
        # TODO - change the filename
        with open('traces/{}.json'.format(time.time()), 'w+') as f:
            json.dump(self.py_trace, f, indent=2)
        self.py_trace = []
