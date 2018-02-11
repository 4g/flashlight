import os

from sanic import Sanic
from sanic.response import json

from flashlight.backend import utility, config

app = Sanic('FlashLight_Server')
app.static('/', '../frontend/build')
app.static('/static', '../frontend/build/static')
app.static('/static/js', '../frontend/build/static/js')
app.static('/index', '../frontend/build/index.html')


@app.route("/")
async def test(request):
    return json({"hello": "world"})


def run(debug=False):
    statusbus = utility.StatusBus()
    if os.path.isdir(config.DATAFOLDER):
        statusbus.status = utility.compact_files(config.DATAFOLDER, config.BIGFILE)
    else:
        statusbus.status = utility.init_homefolder(config.DATAFOLDER, config.BIGFILE)

    if statusbus.status is True:
        statusbus.clear()
        app.run(host="0.0.0.0", port=8000, debug=debug)


if __name__ == '__main__':
    run()
