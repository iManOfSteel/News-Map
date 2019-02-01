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


def download_data():
    with open('reg.json', 'r') as file:
        reg_mapper = json.load(file)
        for region, url in reg_mapper.items():
            code = int(url.split('/')[-1])
            print(region, code)
            with open('mm_news/{}.json'.format(region), 'w') as region_out:
                json.dump(download_region_titles(code), region_out)
