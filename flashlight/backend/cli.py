import argparse

parser = argparse.ArgumentParser(
    description='Flash the light into the darkness of Neural Networks',
    epilog='No more help!!')
parser.add_argument('--dir', help='Flashlight home directory that stores configurations, \
    data needed to store visualization etc.', type=str, dest='FLHOME')
args = parser.parse_args()
