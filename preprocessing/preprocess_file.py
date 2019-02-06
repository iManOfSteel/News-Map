import prepare_text

from natasha import LocationExtractor
from natasha.markup import format_json
from joblib import Parallel, delayed

import pandas as pd
import sys
import os
import json
import time


def remove_locations(news):
    extractor = LocationExtractor()
    matches = extractor(news)
    for match in matches:
        news = news.replace(match.fact.name, '')
    news = news.replace('  ', ' ')
    return news


def prepare_file(path):
    data = pd.read_csv(path, nrows=1000)
    data.fillna('', inplace=True)
    data.news = data.news.apply(lambda x: ' '.join(prepare_text.prepare_text(x)))
    data.news = data.news.apply(remove_locations)
    pd.DataFrame(data.news).to_csv(os.path.join(os.path.dirname(os.path.abspath(path)), 'prepared.csv'))


def parse_text(text):
    return remove_locations(' '.join(prepare_text.prepare_text(text)))


def prepare_file_parallel(path):
    data = pd.read_csv(path)
    data.fillna('', inplace=True)

    parsed_news = Parallel(n_jobs=4)(delayed(parse_text)(data.news[i]) for i in range(len(data.news)))
    pd.DataFrame(parsed_news).to_csv(os.path.join(os.path.dirname(os.path.abspath(path)), 'prepared.csv'))


def main():
    filename = sys.argv[1]
    prepare_file(os.path.abspath(filename))


def parse_kazakstan():
    train_file = open('train.json')
    train_json = json.load(train_file)
    parsed = []
    morph = MorphAnalyzer()
    for item in train_json[:1000]:
        item['text'] = remove_locations(
            ' '.join(filter(morph.word_is_known, prepare_text.prepare_text(item['text']))))
        parsed.append(item)
        print(item['id'])
    parsed_file = open('train_parsed.json', 'w')
    json.dump(parsed, parsed_file)


if __name__ == '__main__':
    cur = time.time()
    prepare_file_parallel(os.path.abspath(sys.argv[1]))
    print(time.time() - cur)