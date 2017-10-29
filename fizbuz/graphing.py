import inspect
import sys
import os
import linecache

traces = []


def grapher(net, x):
    current_frame = inspect.currentframe()
    call_frame = inspect.getouterframes(current_frame)
    with open(call_frame[1].filename) as fp:
        code = compile(fp.read(), 'fizbuz.py', 'exec')
        print(code)


def global_trace(frame, why, arg):
    global traces
    if why == 'call':
        code = frame.f_code
        filename = frame.f_globals.get('__file__', None)
        if filename:
            modulename = filename.split('/')[-1][:-3]
            if modulename is not None:
                traces.append("ModuleName:{}, funcname: {}".format(modulename, code.co_name))
                return local_trace
        else:
            return None


def local_trace(frame, why, arg):
    global traces
    if why == "line":
        # record the file name and line number of every trace
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        bname = os.path.basename(filename)
        traces.append("{} {}: {}".format(bname, lineno, linecache.getline(filename, lineno)))
    return local_trace


sys.settrace(global_trace)
