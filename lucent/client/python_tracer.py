import sys
import linecache


class PythonTracer:
    """ Tracer module that acts as a context manager sets and unsets sys.settrace
    and returns the traced data
    """

    def __init__(self):
        self.trace = []

    def __enter__(self):
        sys.settrace(self._trace_callback)
        return self

    def __exit__(self, type, value, traceback):
        sys.settrace(None)

    def _trace_callback(self, frame, why, arg):
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        if '/torch/' not in filename and 'lucent/client/' not in filename:
            if why == 'call':
                code = frame.f_code
                if filename:
                    self.trace.append((filename, code.co_name, linecache.getline(filename, lineno), '======================='))
                else:
                    raise Exception('Filename is empty')
            if why == "line":
                class_obj = frame.f_locals.get("self", None)
                if class_obj is not None:
                    class_name = class_obj.__class__.__name__
                else:
                    class_name = '<NO_CLASS_NAME>'
                self.trace.append((filename, class_name, lineno, linecache.getline(filename, lineno)))
        return self._trace_callback
