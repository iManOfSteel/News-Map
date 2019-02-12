import pickle
import os

SENTIMENT_DICT_FILE = 'dictionary.pickle'


def init():
    global sentiment_dict
    with open(os.path.join(os.path.dirname(__file__), SENTIMENT_DICT_FILE), 'rb') as file:
        sentiment_dict = pickle.load(file)


def get_text_score(text, wrd_scores=None, w=None, activation=None):
    if wrd_scores is None:
        wrd_scores = sentiment_dict
    if activation is None:
        def activation(x):
            return x
    score = 0
    cnt = 0
    for word in text.split():
        if word in wrd_scores:
            if w is None:
                score += activation(wrd_scores[word])
                cnt += 1
            elif word in w:
                score += activation(wrd_scores[word]) * w[word]
                cnt += 1
    return score / cnt if cnt > 0 else 0
