import re
import os
import json
import pandas

def clean(text):
    if type(text) != str:
        return ''

    url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\\+.~#?&/=]*)'
    word_regex = r'[А-Яа-я]+'

    text = re.sub(url_regex, '', text)
    text = text.lower()
    text = text.replace('ё', 'е')
    text = ' '.join(re.findall(word_regex, text))
    return text

def get_hashtags(text):
    if type(text) != str:
        return ''

    hashtag_regex = r'#[А-Яа-я]+'
    return list(map(lambda x: clean(x[1:]), re.findall(hashtag_regex, text)))

def clean_file_csv(filename):
    data = pandas.read_csv(filename, sep='№%:№%:', engine='python', header=None)
    data[3] = data[0].apply(get_hashtags)
    data[0] = data[0].apply(clean)
    data.to_csv(filename[:filename.find('.')] + '_clean' + filename[filename.find('.'):], sep=',', header=None)

def clean_json_file(filename):
    data = []
    with open(filename, 'r') as file:
        data = json.load(file)
    for i in range(len(data)):
        data[i][0] = clean(data[i][0])

    #print(data)
    clean_file = open(filename[:filename.find('.')] + '_clean' + filename[filename.find('.'):], 'w')
    json.dump(data, clean_file)
    clean_file.close()

if __name__ == '__main__':
    '''files = filter(lambda x: x[:2] == 'pu', os.listdir())
    for file in files:
        print(file)
        clean_file(file)'''
    files = filter(lambda x: x[-5:] == '.json', os.listdir())
    for file in files:
        print(file)
        clean_json_file(file)
