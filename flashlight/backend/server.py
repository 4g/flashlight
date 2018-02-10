import os

from sanic import Sanic
from sanic.response import json

from backend import utility, config


app = Sanic()
app.static('/', '../frontend/build')
app.static('/static', '../frontend/build/static')
app.static('/static/js', '../frontend/build/static/js')
app.static('/index', '../frontend/build/index.html')


@app.route("/")
async def test(request):
    return json({"hello": "world"})


def run(debug=False):
    if os.path.isdir(config.DATAFOLDER):
        utility.compact_files(config.DATAFOLDER, config.BIGFILE)
    else:
        # TODO - excpetion handling
        os.makedirs(config.DATAFOLDER)
    app.run(host="0.0.0.0", port=8000, debug=debug)


if __name__ == '__main__':
    run()
