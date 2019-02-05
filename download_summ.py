import os
import time
import json
import nltk
import random
from multiprocessing.dummy import Pool as ThreadPool
from newspaper import Article
#nltk.download('punkt')


def download_summary(item):
    if random.randint(0, 999) == 0:
        print('Work in progress')
    try:
        url = 'http://' + item[1]
        res = Article(url, language='ru')
        res.download()
        res.parse()
        res.nlp()
        return res.summary
    except Exception as e:
        pass
    try:
        url = 'https://' + item[1]
        res = Article(url, language='ru')
        res.download()
        res.parse()
        res.nlp()
        return res.summary
    except Exception as e:
        pass


def download_reg_news(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    pool = ThreadPool(15)
    res = list(filter(None, pool.map(download_summary, data)))
    print ('Succ rate = {}%'.format(100.0 * len(res) / len(data)))
    return res


def main():
    reg_folder = 'News-Map/scrapper/mm_news'

    for item in os.listdir(reg_folder)[1:]:
        start = time.time()
        summ = download_reg_news(os.path.join(reg_folder, item))
        with open(os.path.join('summ', item), 'w') as f:
            json.dump(summ, f, ensure_ascii=False)
        print(time.time() - start)


if __name__ == '__main__':
    main()
