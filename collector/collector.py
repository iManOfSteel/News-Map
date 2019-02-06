import pandas as pd
import os
import sys
import json
import re


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'id_city.json')) as f:
    id_city = json.load(f)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'city_region.json')) as f:
    city_region = json.load(f)


def clean(text):
    if type(text) != str:
        return ''

    text = text.lower()
    text = text.replace('ё', 'е')
    return text


def get_hashtags(text):
    if type(text) != str:
        return ''

    hashtag_regex = r'#[А-Яа-я]+'
    return list(map(lambda x: clean(x[1:]), re.findall(hashtag_regex, text)))


def concat_json1(path):
    json_files = list(filter(lambda x: x[-5:]  == '.json', os.listdir(path)))

    media = []
    for json_file in json_files:
        with open(path + '/' + json_file, 'r') as file:
            media += map(lambda x: [x, json_file[:-5].lower()], json.load(file))

    media = pd.DataFrame(media)
    media.rename({0: 'news', 1: 'city'}, axis="columns", inplace=True)

    media['city'] = media.city.apply(clean)
    media.news = media.news.apply(lambda x: x.replace('\n', ' '))
    media['date'] = ''
    media['tags'] = '[]'
    media['clarification'] = ''
    media['region'] = media.city.apply(lambda x: city_region[x])
    media['link'] = ''

    media.to_csv(path + '/collected.csv')


def concat_json2(path):
    json_files = list(filter(lambda x: x[-5:]  == '.json', os.listdir(path)))

    media = []
    for json_file in json_files:
        with open(os.path.join(path, json_file), 'r') as file:
            media += map(lambda x: [x[0], x[1], json_file[:-5].lower()], json.load(file))

    media = pd.DataFrame(media)
    media.rename({0: 'news', 1: 'link', 2: 'city'}, axis="columns", inplace=True)
    media['city'] = media.city.apply(clean)
    media['date'] = ''
    media['tags'] = '[]'
    media['clarification'] = ''
    media['region'] = media.city.apply(lambda x: city_region[x])

    media.to_csv(path + '/collected.csv')


def concat_csv(path, delim='№%:№%:'):
    csv_files = list(filter(lambda x: x[:2] == 'pu', os.listdir(path)))
    vk_publics = []
    for csv_file in csv_files:
        vk_publics.append(pd.read_csv(path + '/' + csv_file, sep=delim, engine='python', header=None))
    vk_publics = pd.concat(vk_publics, sort=True, ignore_index=True)

    vk_publics.rename({0: 'news', 1: 'date', 2: 'link'}, axis="columns", inplace=True)

    vk_publics['tags'] = vk_publics.news.apply(get_hashtags)
    # vk_publics['news'] = vk_publics['news'].apply(clean)
    vk_publics['clarification'] = ''
    vk_publics['city'] = vk_publics.link.apply(lambda x: clean(id_city[str(x)]))
    vk_publics['region'] = vk_publics.city.apply(lambda x: city_region[x])

    links = vk_publics.link.apply(lambda x: 'vk.com/public' + str(x))
    vk_publics.drop('link', inplace=True, axis=1)
    vk_publics['link'] = links

    vk_publics.to_csv(path + '/collected.csv')


def main():
    file_type = sys.argv[1]
    path = sys.argv[2]

    if file_type == 'json1':
        concat_json1(path)
    elif file_type == 'json2':
        concat_json2(path)
    elif file_type == 'csv':
        if len(sys.argv) >= 4:
            concat_csv(path, sys.argv[3])
        else:
            concat_csv(path)


if __name__ == '__main__':
    main()