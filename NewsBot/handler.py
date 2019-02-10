import requests
import xml.etree.ElementTree

OSM_API = 'https://nominatim.openstreetmap.org/reverse'

area_score = {'хабаровский край': 2.5, 'киренский район': 2}


def process_map(message):
    return 'https://bit.ly/2BoyLbN'


def process_article(text):
    if 'путин' in text.lower():
        raise Exception


def process_reg(longitude=None, latitude=None):
    response = requests.get(OSM_API + '?lat=' + str(latitude) + '&lon=' + str(longitude))
    xml_tree = xml.etree.ElementTree.fromstring(response.content.decode('utf-8'))
    print(xml_tree)
    if len(xml_tree) != 2:
        return None

    address_parts = xml_tree[1]
    areas = {address_part.tag: address_part.text.lower() for address_part in address_parts}
    
    area_names = ['hamlet', 'village', 'town', 'city', 'county', 'state', 'country']
    for area_name in area_names:
        if area_name in areas and areas[area_name] in area_score:
            return (areas[area_name], area_score[areas[area_name]])
