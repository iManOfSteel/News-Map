import nltk
import re
from pymystem3 import Mystem
from natasha import LocationExtractor
from nltk.corpus import stopwords
from string import punctuation


RUSSIAN_STOPWORDS = stopwords.words('russian')
RUSSIAN_STOPWORDS.remove('не')
lemmatizer = Mystem()


def delete_locations(news):
    extractor = LocationExtractor()
    matches = extractor(news)
    if len(matches) == 0:
        return news
    result = news[:matches[0].span[0]]
    for i in range(len(matches) - 1):
        result += news[matches[i].span[1]: matches[i + 1].span[0]].strip()
    result += news[matches[-1].span[1]:]
    return result


def lemmatize_text(text):
    return list(filter(None, map(lambda x: x.strip(),
                                 lemmatizer.lemmatize(text))))


def remove_stopwords(tokenized_text):
    return list(filter(lambda x: x not in RUSSIAN_STOPWORDS, tokenized_text))


def remove_not_words_punct(tokenized_text):
    ans = []
    word_regex = re.compile(r'([А-Яа-я]|[-,.!?();:])')
    for token in tokenized_text:
        good = True
        for char in token:
            if word_regex.match(char) is None:
                good = False
        if good:
            ans.append(token)
    return ans


def is_wordlike(token):
    if len(token) >= 3 and token[:3] == 'не_':
        return len(token) > 3 and token[3].isalpha()
    else:
        return len(token) > 0 and token[0].isalpha()


def remove_not_words(tokenized_text):
    return list(filter(is_wordlike, tokenized_text))


def process_negation(tokenized_text):
    ans = []
    to_negate = False
    for token in tokenized_text:
        if token == 'не':
            to_negate = True
        else:
            if token in punctuation:
                to_negate = False
            if to_negate:
                ans.append('не_' + token)
            else:
                ans.append(token)
    return ans


def photo_news_delete(tokenized_text):
    return len(tokenized_text) <= 3 and 'фото' in tokenized_text


def prepare_text(text,
                 process_not=True, # не люблю -> не_люблю
                 words_only=True, # remove all except russian words
                 lemmatize=True, # lemmatize
                 remove_stop_words=True, #remove stop words
                 photo_to_delete=True):

    text = text.lower()
    text = text.replace('ё', 'е')

    if lemmatize:
        processed = lemmatize_text(text)
    else:
        processed = nltk.word_tokenize(text)

    if remove_stop_words:
        processed = remove_stopwords(processed)

    processed = remove_not_words_punct(processed)

    if process_not:
        processed = process_negation(processed)

    if words_only:
        processed = remove_not_words(processed)

    if photo_to_delete and photo_news_delete(processed):
        processed = list()

    return processed


def process_text(text):
    return ' '.join(prepare_text(delete_locations(text)))
