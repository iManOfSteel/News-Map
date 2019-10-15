import requests
import json
import score_text
import xml.etree.ElementTree

OSM_API = 'https://nominatim.openstreetmap.org/reverse'

with open('reg_scores.json') as f:
    area_score = json.load(f)


def process_map(message):
    return 'https://bit.ly/2BAbS5m'


def process_article(text):
    return score_text.analyze_text(text)

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

def process_reg_text(loc_name):
    loc_name = loc_name.lower()
    if loc_name in area_score:
        return area_score[loc_name]
    loc_name = 'городской округ {}'.format(loc_name)
    return area_score[loc_name]
