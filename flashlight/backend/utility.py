import os
import json


def compact_files(folder, outfile):
    # load from outfile if exists
    try:
        with open(outfile, 'r') as f:
            full = json.load(f)
    except FileNotFoundError:
        full = []

    # add to outfile data
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), 'r') as f:
            try:
                full.append(json.load(f))
            except json.decoder.JSONDecodeError:
                print('FlashlightHome has files those are not JSON friendly, exiting..')
                return False

    try:
        # doing another loop since removing the file in previous loop could
        # cause data lose if user stops the process in between
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))

        # writing outfile
        with open(outfile, 'w+') as f:
            json.dump(full, f)
    except PermissionError:
        print("FlashLight doesn't have permission to use it's own home, exiting...")
        return False

    return True


def init_homefolder(folder, outfile):
    try:
        os.makedirs(folder)
        with open(outfile, 'w+') as f:
            json.dump([], f)
    except PermissionError:
        print("FlashLight doesn't have permission to use it's own home, exiting...")
        return False
    return True


def get_root_path(current):
    return os.path.dirname(os.path.dirname(os.path.realpath(current)))


class StatusBus:
    """ Channel that keeps the status from different fucntions """

    def __init__(self):
        self._status = []

    @property
    def status(self):
        return all(self._status)

    @status.setter
    def status(self, val):
        if isinstance(val, bool):
            self._status.append(val)
        else:
            raise Exception('Cannot add non-bool value to status bus')

    def clear(self):
        self._status = []
