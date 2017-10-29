import inspect


def grapher(net, x):
    current_frame = inspect.currentframe()
    call_frame = inspect.getouterframes(current_frame)
    with open(call_frame[1].filename) as fp:
        code = compile(fp.read(), 'fizbuz.py', 'exec')
        print(code)
