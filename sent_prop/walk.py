import gensim
import numpy as np
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter


def get_popular_words(texts, num=10000):
    words = list(map(lambda x: x[0], Counter(' '.join(texts)).most_common(num)))
    return words


def get_edge_matrix(embeddings, k=25):
    A = np.array([embeddings[word] for word in embeddings.iw])
    T = cosine_similarity(A)
    T = np.arccos(np.clip(-T, -1, 1)) / np.pi
    def knn(vec, k=k):
        vec[vec < np.argsort(vec)[-k]] = 0.
    np.fill_diagonal(T, 0)
    np.apply_along_axis(knn, 1, T)
    return T


def get_dict_from_csv(filename):
    doc = pd.read_csv(filename)
    return get_dict(doc['news'])


def transition_matrix(embeddings):
    edge_matrix = get_edge_matrix(embeddings)
    scale_matrix = np.diag([1. / np.sqrt(edge_matrix[i].sum())
                            if edge_matrix[i].sum() > 0. else 0.
                            for i in range(edge_matrix.shape[0])])
    return np.dot(scale_matrix, np.dot(edge_matrix, scale_matrix))


def random_walk(embeddings, positive_seeds, negative_seeds, beta=0.9, max_iter=50, eps=1e-6):
    if not type(positive_seeds) == dict:
        positive_seeds = {word: 1.0 for word in positive_seeds}

    if not type(negative_seeds) == dict:
        negative_seeds = {word: 1.0 for word in negative_seeds}

    words = embeddings.iw
    tr_matrix = transition_matrix(embeddings)
    pos_pol = run_walk(tr_matrix, get_walk_start_vector(words, positive_seeds), beta)
    neg_pol = run_walk(tr_matrix, get_walk_start_vector(words, negative_seeds), beta)
    return {w: pos_pol[i] / (neg_pol[i] + pos_pol[i]) for i, w in enumerate(words)}


def run_walk(tr_matrix, pol_vector, beta, max_iter, eps):
    for i in range(max_iter):
        print('walking {}:{}'.format(i, max_iter))
        new_vector = beta * np.dot(tr_matrix, pol_vector) + (1 - beta) * pol_vector
        if np.abs(new_vector - pol_vector).sum() < eps:
            break
        pol_vector = new_vector
    return pol_vector


def get_walk_start_vector(words, seeds):
    return np.array([seeds[word] if word in seeds else 0.0 for word in words])

def get_trained_model(data_file='data.csv', wv_file='wiki.ru.vec'):
    positive_seeds = ["хороший", "прекрасный", "счастливый", "улучшение", "прогресс", "успех", "добро"]
    negative_seeds = ["ненависть", "ужасный", "несчастный", "трагедия", "плохой", "зло", "смерть"]

    embeddings = gensim.models.KeyedVectors.load_word2vec_format(wv_file) 
    embeddings.iw = get_dict_from_csv(data_file)
    random_walk(embeddings, positive_seeds, negative_seeds)

if __name__ == "__main__":
    get_trained_model()
