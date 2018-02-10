import os
from pathlib import Path


FLHOME = '.flashlight'
USERHOME = str(Path.home())
BIGFILE = os.path.join(USERHOME, FLHOME, 'big.json')
DATAFOLDER = os.path.join(USERHOME, FLHOME, 'data')
