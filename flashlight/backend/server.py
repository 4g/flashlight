import os

from sanic import Sanic
from sanic.response import json
from sanic.log import logger

from flashlight.backend import utility, config

root_path = utility.get_root_path(__file__)
app = Sanic('FlashLight_Server')
app.static('/', os.path.join(root_path, 'frontend/build'))
app.static('/static', os.path.join(root_path, 'frontend/build/static'))
app.static('/static/js', os.path.join(root_path, 'frontend/build/static/js'))
app.static('/index', os.path.join(root_path, 'frontend/build/index.html'))


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
        logger.info('Starting FlashLight server using Sanic')
        app.run(host=config.HOST, port=config.PORT, debug=debug)


if __name__ == '__main__':
    run()
