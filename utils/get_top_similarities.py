import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity


def load_embedding(path):
    return np.loadtxt(path)


def get_top_similarities(embedding_matrix, index, top_k):
    similarities_matrix = calculate_similarities_matrix(embedding_matrix)
    result_relevance = similarities_matrix[index]
    relevance_orders = np.argsort(result_relevance)[::-1]  # desc
    # print('relevance_orders: ', relevance_orders)
    return relevance_orders[:top_k]


def calculate_similarities_matrix(matrix):
    A_sparse = sparse.csr_matrix(matrix)
    matrix_similarities = cosine_similarity(A_sparse)
    print('pairwise dense output:\n {}\n'.format(matrix_similarities))
    return matrix_similarities


if __name__ == "__main__":
    embedding_path = '/Volumes/DATA/workspace/aus/aus-graphembedding/output/matrix_semantic.out'
    embedding_matrix = load_embedding(embedding_path)

    ids = get_top_similarities(embedding_matrix, index=1, top_k=5)
    print (ids)
