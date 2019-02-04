import numpy as np


def get_edge_matrix(embeddings):
    matrix = np.dot(embeddings.matrix, np.transpose(embeddings.matrix))
    matrix = np.arccos(np.clip(-matrix, -1, 1))/np.pi
    np.fill_diagonal(matrix, 0)



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
        new_vector = beta * np.dot(tr_matrix, pol_vector) + (1 - beta) * pol_vector
        if np.abs(new_vector - pol_vector).sum() < eps:
            break
        pol_vector = new_vector
    return pol_vector


def get_walk_start_vector(words, seeds):
    return np.array([seeds[word] if word in seeds else 0.0 for word in words])