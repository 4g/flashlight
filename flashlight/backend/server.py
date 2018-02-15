import os

from sanic import Sanic
from sanic.log import logger

from flashlight.backend import utility, config

root_path = utility.get_root_path(__file__)
app = Sanic('FlashLight_Server')
app.static('/', os.path.join(root_path, 'frontend/build'))
app.static('/static', os.path.join(root_path, 'frontend/build/static'))
app.static('/static/js', os.path.join(root_path, 'frontend/build/static/js'))
app.static('/', os.path.join(root_path, 'frontend/build/index.html'))


def run(debug=False):
    bus = utility.Bus()
    if os.path.isdir(config.DATAFOLDER):
        bus.status = utility.compact_files(config.DATAFOLDER, config.BIGFILE)
    else:
        bus.status = utility.init_homefolder(config.DATAFOLDER, config.BIGFILE)

    if bus.status is True:
        bus.clear()
        logger.info('Starting FlashLight server using Sanic')
        app.run(host=config.HOST, port=config.PORT, debug=debug)


if __name__ == '__main__':
    run()
