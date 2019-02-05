import nltk
import re
from pymystem3 import Mystem
from nltk.corpus import stopwords
from string import punctuation


RUSSIAN_STOPWORDS = stopwords.words('russian')
RUSSIAN_STOPWORDS.remove('не')


def lemmatize_text(text):
    lemmatizer = Mystem()
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
    return token.isalpha() or (len(token) > 3 and token[3:].isalpha())


def remove_not_words(tokenized_text):
    return list(filter(lambda token: len(token) > 0 and is_wordlike(token),
                       tokenized_text))


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


def prepare_text(text: str,
                 process_not=True, # не люблю -> не_люблю
                 words_only=True, # remove all except russian words
                 lemmatize=True, # lemmatize
                 remove_stop_words=True, #remove stop words
                 min_tf=100, # min word freq
                 max_tf = 0.9):

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

    return processed
