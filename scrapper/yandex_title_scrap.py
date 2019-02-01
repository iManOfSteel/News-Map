import requests
import time
from bs4 import BeautifulSoup

'''
BASE_YANDEX_URL = 'https://news.yandex.ru/yandsearch'
CGI_ARGS = {'rpt': 'nnews2',
            'geonews': None,
            'within': 777,
            'from_day': None,
            'from_month': None,
            'from_year': None,
            'to_day': None,
            'to_month': None,
            'to_year': None,
            'p': 0}
'''

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
    print(rows)
    return rows


def download_region_titles(region_code):
    url = BASE_MM_URL.format(region_code, 'html', 1)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    page_number = get_page_number(soup)

    titles = list()
    titles += get_titles(region_code, 1)

    for cur_page in range(2, page_number + 1):
        titles += get_titles(region_code, cur_page)
        print(len(titles))


def main():
    download_region_titles(818)


main()
