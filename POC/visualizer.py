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
        print(graph_from_tracer)
        # TODO - remove assumption that input is always a single tensor
        model_params = [x] + list(self.net.parameters())
        input_nodes = list(graph_from_tracer.inputs())
        internal_nodes = list(graph_from_tracer.nodes())
        for meta, value in zip(input_nodes, model_params):
            # TODO -  convert display_Values to json serailizable
            graph[meta.unique()] = {
                'display_values': value.size(),
                'display_type': 'tensor',
                'dependancies': [],
                'dependands': self._get_user_ids(meta.uses()),
                'node_name': meta.kind(),
                'datatype': meta.type().scalarType(),
                'shape': meta.type().sizes()}
        for node in internal_nodes:
            try:
                datatype = node.type().scalarType()
            except Exception as e:
                print(node.type(), node)
                datatype = 'Unknown'

            try:
                shape = node.type().sizes()
            except Exception as e:
                shape = 'Unknown'

            graph[node.unique()] = {
                'display_values': None,
                'display_type': None,
                'dependancies': self._get_node_ids(node.inputs()),
                'dependands': self._get_user_ids(node.uses()),
                'node_name': node.kind(),
                'datatype': datatype,
                'shape': shape}
        # print(json.dumps(graph, indent=2))

    def _fill_unknown(val, unknown='Unknown'):
        pass

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
"""
{
  "1": {
    "display_values": [
      64,
      10
    ],
    "display_type": "tensor",
    "dependancies": [],
    "dependands": [
      8
    ],
    "node_name": "Param",
    "datatype": "Float",
    "shape": [
      64,
      10
    ]
  },
  "2": {
    "display_values": [
      100,
      10
    ],
    "display_type": "tensor",
    "dependancies": [],
    "dependands": [
      6
    ],
    "node_name": "Param",
    "datatype": "Float",
    "shape": [
      100,
      10
    ]
  },
  "3": {
    "display_values": [
      100
    ],
    "display_type": "tensor",
    "dependancies": [],
    "dependands": [
      7
    ],
    "node_name": "Param",
    "datatype": "Float",
    "shape": [
      100
    ]
  },
  "4": {
    "display_values": [
      4,
      100
    ],
    "display_type": "tensor",
    "dependancies": [],
    "dependands": [
      10
    ],
    "node_name": "Param",
    "datatype": "Float",
    "shape": [
      4,
      100
    ]
  },
  "5": {
    "display_values": [
      4
    ],
    "display_type": "tensor",
    "dependancies": [],
    "dependands": [
      11
    ],
    "node_name": "Param",
    "datatype": "Float",
    "shape": [
      4
    ]
  },
  "6": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      2
    ],
    "dependands": [
      8
    ],
    "node_name": "t",
    "datatype": "Float",
    "shape": [
      10,
      100
    ]
  },
  "7": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      3
    ],
    "dependands": [
      8
    ],
    "node_name": "expand",
    "datatype": "Float",
    "shape": [
      64,
      100
    ]
  },
  "8": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      7,
      1,
      6
    ],
    "dependands": [
      9
    ],
    "node_name": "addmm",
    "datatype": "Float",
    "shape": [
      64,
      100
    ]
  },
  "9": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      8
    ],
    "dependands": [
      12
    ],
    "node_name": "sigmoid",
    "datatype": "Float",
    "shape": [
      64,
      100
    ]
  },
  "10": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      4
    ],
    "dependands": [
      12
    ],
    "node_name": "t",
    "datatype": "Float",
    "shape": [
      100,
      4
    ]
  },
  "11": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      5
    ],
    "dependands": [
      12
    ],
    "node_name": "expand",
    "datatype": "Float",
    "shape": [
      64,
      4
    ]
  },
  "12": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      11,
      9,
      10
    ],
    "dependands": [
      13
    ],
    "node_name": "addmm",
    "datatype": "Float",
    "shape": [
      64,
      4
    ]
  },
  "13": {
    "display_values": null,
    "display_type": null,
    "dependancies": [
      12
    ],
    "dependands": [
      0
    ],
    "node_name": "sigmoid",
    "datatype": "Float",
    "shape": [
      64,
      4
    ]
  }
}
"""