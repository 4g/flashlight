import sys
import os
import linecache


class Visualizer:
    """
    Base visualization class
    """

    def __init__(self):
        self.traces = []

    def round_a_loop(self):
        sys.settrace(self._global_trace)

    def _global_trace(self, frame, why, arg):
        if why == 'call':
            code = frame.f_code
            filename = frame.f_globals.get('__file__', None)
            if filename:
                # TODO - check filename always means modulename with value or not
                self.traces.append((filename, code.co_name))
                return self._local_trace
            else:
                return None

    def _local_trace(self, frame, why, arg):
        global traces
        if why == "line":
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            bname = os.path.basename(filename)
            self.traces.append((bname, lineno, linecache.getline(filename, lineno)))
        return self._local_trace
