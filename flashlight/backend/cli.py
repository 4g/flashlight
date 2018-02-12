import argparse

parser = argparse.ArgumentParser(
    description='Flash the light into the darkness of Neural Networks',
    epilog='No more help!!')
parser.add_argument(
    '--dir', help='Flashlight home directory that stores configurations, \
    data needed to store visualization etc.', type=str, dest='FLHOME')
parser.add_argument(
    '--host', help='IP address flashlight server uses', type=str, dest='HOST')
parser.add_argument(
    '--port', help='Port address flashlight server uses', type=str, dest='PORT')
args = parser.parse_args()

if __name__ == '__main__':
    print(args)
