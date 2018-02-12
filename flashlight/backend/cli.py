import os
import argparse
from pathlib import Path


USERHOME = str(Path.home())


parser = argparse.ArgumentParser(
    description='Flash the light into the darkness of Neural Networks',
    epilog='No more help!!')

parser.add_argument(
    '--dir', help='Flashlight home directory',
    default=os.path.join(USERHOME, '.flashlight'), type=str, dest='FLHOME')
parser.add_argument(
    '--host', help='IP address flashlight server uses',
    default='0.0.0.0', type=str, dest='HOST')
parser.add_argument(
    '--port', help='Port address flashlight server uses',
    default='8000', type=str, dest='PORT')
args = parser.parse_args()

if __name__ == '__main__':
    print(args)
