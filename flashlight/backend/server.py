import os
from pathlib import Path

from sanic import Sanic
from sanic.response import json

from backend import utility


app = Sanic()
app.static('/', '../frontend/build')
app.static('/static', '../frontend/build/static')
app.static('/static/js', '../frontend/build/static/js')
app.static('/index', '../frontend/build/index.html')

bigfile = 'big.json'
# TODO - make it configurable
flashlight_home = '.flashlight'


@app.route("/")
async def test(request):
    return json({"hello": "world"})


def run(debug=False):
    full_path = os.path.join(str(Path.home()), flashlight_home)
    if os.path.isdir(full_path):
        utility.compact_files(full_path, bigfile)
    else:
        # TODO - excpetion handling
        os.makedirs(full_path)
    app.run(host="0.0.0.0", port=8000, debug=debug)


if __name__ == '__main__':
    run()
