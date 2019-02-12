import json
import pickle
import os
import sys
import operator
from osm_area import OSMArea

LEVELS = 4


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


def summate_second_type(number_dict):
    result = dict()
    for element in number_dict.values():
        found = result.get(element[0], (0., 0))
        result[element[0]] = tuple(map(operator.add, found, (element[1], element[2])))
    return result


def decode_number_dict_to_named(filename_dict: str, filename_area: str):
    with open(os.path.expanduser(os.path.realpath(filename_dict)), 'r') as file:
        number_dict = json.load(file)

    print('\n'.join(map(str, list(number_dict.values()))))

    if type(list(number_dict.values())[0]) != float:
        number_dict = summate_second_type(number_dict)

    linearized = load_linearized(filename_area)
    for x, y in number_dict.items():
        print(x, int(x))
        pass
    return {linearized[int(x)]: y for x, y in number_dict.items() if int(x) != 0}


def main(filename_dict: str, filename_area: str, filename_out: str):
    named_dict = decode_number_dict_to_named(filename_dict, filename_area)
    with open(os.path.expanduser(os.path.relpath(filename_out)), 'w') as file:
        json.dump(named_dict, file)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
