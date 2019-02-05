import os
import time
import json
import nltk
import random
from multiprocessing.dummy import Pool as ThreadPool
from newspaper import Article
#nltk.download('punkt') # run this 1 time


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


DATA_FOLDER = '../data'
DOWNLOAD_FOLDER = os.path.join(DATA_FOLDER, 'summaries/')
REG_FOLDER = os.path.join(DATA_FOLDER, 'first_ver/mediametrics/')


def main():
    print('Starting download of summaries')
    print('They will be saved in', os.path.abspath(DOWNLOAD_FOLDER))
    print('The folder with reg files is', os.path.abspath(REG_FOLDER))

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    for item in os.listdir(REG_FOLDER):
        start = time.time()
        summaries = download_reg_news(os.path.join(REG_FOLDER, item))
        with open(os.path.join(DOWNLOAD_FOLDER, item), 'w') as f:
            json.dump(summ, f, ensure_ascii=False)
        print(time.time() - start)

