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
        with open(file, 'r') as f:
            full.append(json.load(f))

    # writing outfile
    with open(outfile, 'w+') as f:
        json.dump(full, f)

    # doing another loop since removing the file in previous loop could
    # cause data lose if user stops the process in between
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))
