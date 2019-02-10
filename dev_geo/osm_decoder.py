import json
import pickle
import os
import sys


LEVELS = 4


class OSMArea:
    def __init__(self, name=None, idd=None, level=1, members=None):
        self.level = level
        self.id = idd
        self.members = members
        if members is None:
            self.members = list()
        self.name = name

    def __repr__(self):
        return 'OSMArea {} {}'.format(self.name, self.id)


def deep_search(area, level=LEVELS):
    yield (area.id, area.name)
    if level > 0:
        for mem in area.members:
            yield from deep_search(mem, level-1)


def load_linearized(filename: str):
    with open(os.path.expanduser(os.path.realpath(filename)), 'rb') as file:
        pickled = pickle.load(file)
    linearized = dict(list(deep_search(pickled)))
    return linearized


def decode_number_dict_to_named(filename_dict: str, filename_area: str):
    with open(os.path.expanduser(os.path.realpath(filename_dict)), 'r') as file:
        number_dict = json.load(file)
    linearized = load_linearized(filename_area)
    return {linearized[int(x)]: y for x, y in number_dict.items()}


def main(filename_dict: str, filename_area: str, filename_out: str):
    named_dict = decode_number_dict_to_named(filename_dict, filename_area)
    with open(os.path.expanduser(os.path.relpath(filename_out)), 'w') as file:
        json.dump(named_dict, file)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
