import requests
import json
from bs4 import BeautifulSoup

BASE_MM_URL = 'https://mediametrics.ru/rating/ru/{}/month.{}?page={}'


def get_page_number(page_soup: BeautifulSoup):
    paging = page_soup.find('div', class_='paging')
    try:
        return int(paging.div.find_all('a')[-2].text)
    except AttributeError:
        return -1


def get_titles(region_code, page):
    tsv_url = BASE_MM_URL.format(region_code, 'tsv', page)
    response = requests.get(tsv_url)
    rows = [tup.split('\t') for tup in response.text.split('\n')[1:-2]]
    rows = [(tup[1].replace('&quot;', '"'), tup[0]) for tup in rows]
    return rows


def download_region_titles(region_code):
    url = BASE_MM_URL.format(region_code, 'html', 1)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    page_number = get_page_number(soup)

    titles = list()
    for title in get_titles(region_code, 1):
        titles.append(title)

    for cur_page in range(2, page_number + 1):
        for title in get_titles(region_code, cur_page):
            titles.append(title)
        print(len(titles))
    return titles


REGION_FILE = 'reg2.json'
OLD_REGION_FILE = 'reg.json'
DELTA_FILE = 'delta.json'


def download_data(reg_file):
    with open(reg_file, 'r') as file:
        reg_mapper = json.load(file)
        for region, url in reg_mapper.items():
            code = int(url.split('/')[-1])
            print(region, code)
            with open('mm_news/{}.json'.format(region), 'w') as region_out:
                json.dump(download_region_titles(code), region_out)


def write_new_regions(reg_file, old_file, delta_file):
    old_dict = dict()
    new_dict = dict()
    with open(old_file, 'r') as file:
        old_dict = json.load(file)
    with open(reg_file, 'r') as file:
        new_dict = json.load(file)

    left_regions = list(filter(None, map(lambda tup: tup if tup[0] not in old_dict else '',
                                         new_dict.items())))

    formatted = {x[0]: x[1].split('/month.html')[-2] for x in left_regions}
    with open(delta_file, 'w') as file:
        json.dump(formatted, file)
