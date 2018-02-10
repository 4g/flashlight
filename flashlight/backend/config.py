import os
from pathlib import Path

from flashlight.backend import cli


USERHOME = str(Path.home())
FLHOME = cli.args.FLHOME or os.path.join(USERHOME, '.flashlight')
BIGFILE = os.path.join(FLHOME, 'big.json')
DATAFOLDER = os.path.join(FLHOME, 'data')
