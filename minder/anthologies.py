import os
from minder.core import anthologies_dirpath
from minder.viewing import run_viewer

anthologies_names = os.listdir(anthologies_dirpath)

anthologies = {}

for anthology_name in anthologies_names:
    anthology_filepath = os.path.join(anthologies_dirpath, anthology_name)
    with open(anthology_filepath) as anthology_file:
        note_names = [
            name for name in anthology_file.read().splitlines() if len(name) > 0 and name[0] != '#'
        ]
    anthologies[anthology_name] = note_names


def open_anthology(anthology_name):
    note_names = anthologies[anthology_name]
    run_viewer(note_names)
