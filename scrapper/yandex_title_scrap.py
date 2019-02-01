import requests
import time
from bs4 import BeautifulSoup


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
GENRE = 'Сообщения'


def construct_cgi_url(base_url, cgi_args):
    return base_url + '?' + '&'.join(['{}={}'.format(elem[0], elem[1])
                                      for elem in cgi_args.items()])


def get_article_number(page_soup: BeautifulSoup):
    tags = page_soup.find_all('span', class_='radiobox__text')
    for tag in tags:
        label = tag.find('span', class_='filters__label')
        if label is not None:
            return int(tag.find('span', class_='filters__counters').text)
    raise Exception("Something's wrong")


def main():


    cur_args = dict(CGI_ARGS)
    cur_args['geonews'] = 49  # Penza
    cur_args['from_day'] = '01'
    cur_args['from_month'] = '11'
    cur_args['from_year'] = '2018'
    cur_args['to_day'] = '01'
    cur_args['to_month'] = '02'
    cur_args['to_year'] = '2019'
    print(construct_cgi_url(BASE_YANDEX_URL, cur_args))
    # page_text = http.request('GET', construct_cgi_url(BASE_YANDEX_URL, cur_args)).data
    page_text = requests.get(construct_cgi_url(BASE_YANDEX_URL, cur_args))
    page_text.encoding = 'utf-8'
    print(page_text.text)
    print('radiobox' in page_text.text)
    soup = BeautifulSoup(page_text.text, 'html.parser')
    article_number = get_article_number(soup)
    cur_number = 0
    start_time = time.time()
    while cur_number < article_number:
        cur_args['p'] += 1
        print(construct_cgi_url(BASE_YANDEX_URL, cur_args))
        cur_page = http.request('GET', construct_cgi_url(BASE_YANDEX_URL, cur_args)).data

        cur_soup = BeautifulSoup(cur_page, 'html.parser')
        all_news = soup.find_all('div', class_='document__title')
        for news in all_news:
            cur_number += 1
            if cur_number % 1000 == 0:
                print(cur_number)
                print(time.time() - start_time)
            # print(news.a.text)  # ????


main()
