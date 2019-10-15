import pickle
import overpy
from multiprocessing import Pool
from osm_area import OSMArea


def download_towns(rel_area: OSMArea):
    try:
        api2 = overpy.Overpass()
        api2.url = 'https://overpass.kumi.systems/api/interpreter'
        result = api2.query("""rel({}); map_to_area; (rel[boundary="administrative"](area); 
                                rel[place~"city|town"](area);); out;"""
                            .format(rel_area.id))
        try:
            current = next(v for v in result.relations if v.tags.get('name', '') == rel_area.name)
        except StopIteration:
            current = None
        rel_area.members = list(
            map(
                lambda x: OSMArea(idd=x.id, name=x.tags['name']), 
                filter(
                    lambda x: 
                        'name' in x.tags and
                        x.tags['name'] != rel_area.name and
                        'admin_level' in x.tags and
                        (x.tags['admin_level'] > current.tags['admin_level']
                            if current is not None and 'admin_level' in current.tags
                            else True),
                    result.relations
                )
            )
        )
    except Exception as e:
        print(rel_area, e)
        pass
    return len(rel_area.members)


rayonlist = list()


def deep_search(area: OSMArea, level):
    if level > 0:
        for mem in area.members:
            deep_search(mem, level-1)
    else:
        rayonlist.append(area)
        

with open('osm_numbers.pickle', 'rb') as file:
    russia_area = pickle.load(file)
deep_search(russia_area, 3)
for elem in rayonlist:
    download_towns(elem)
with open('new_numbers2.pickle', 'wb') as file:
    pickle.dump(russia_area, file)

