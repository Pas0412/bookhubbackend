import hashlib
import timeit

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from pandas.api.types import CategoricalDtype
from .models import Books, Rating


def hash_password(password):
    # 将密码转换为字节串
    password_bytes = password.encode('utf-8')
    # 使用 md5 算法进行加密
    hash_obj = hashlib.md5(password_bytes)
    # 返回加密后的结果
    return hash_obj.hexdigest()


def load_data():
    books = Books.objects.all().values_list('bookId', 'title')
    ratings = Rating.objects.all().values_list('userId', 'bookId', 'rating')

    books_df = pd.DataFrame.from_records(books, columns=['bookId', 'title'])
    ratings_df = pd.DataFrame.from_records(ratings, columns=['userId', 'bookId', 'rating'])

    return books_df, ratings_df


class KNN:
    def __init__(self):
        self.knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=7)
        self.fitted = False

    def preprocess(self, books, ratings):
        # Merge books and ratings data
        combine_book_rating = pd.merge(ratings, books, on='bookId')
        combine_book_rating = combine_book_rating.dropna(axis=0, subset=['bookId'])
        return combine_book_rating

    def create_total_data_matrix(self, combine_book_rating):
        combine_book_rating = combine_book_rating
        user_rating = combine_book_rating.drop_duplicates(['userId', 'bookId'])
        user_u = list(sorted(user_rating.userId.unique()))
        ISBN_u = list(sorted(user_rating.bookId.unique()))
        row = user_rating.bookId.astype(CategoricalDtype(categories=ISBN_u)).cat.codes
        col = user_rating.userId.astype(CategoricalDtype(categories=user_u)).cat.codes
        data = user_rating['rating'].tolist()
        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(ISBN_u), len(user_u)))
        df = pd.DataFrame.sparse.from_spmatrix(sparse_matrix, index=ISBN_u, columns=user_u).fillna(0)
        return df, sparse_matrix

    def find_nearest_neighbors(self, book_id, combine_book_rating):
        # Find the index of the input book
        total_data_frame, total_sparse_matrix = self.create_total_data_matrix(combine_book_rating)
        query_index = total_data_frame.index.get_loc(book_id)

        if not self.fitted:
            self.knn.fit(total_sparse_matrix)
            self.fitted = True

        # Find nearest neighbors
        numpy_values = np.array(total_data_frame.iloc[query_index, :].values)
        distances, indices = self.knn.kneighbors(numpy_values.reshape(1, -1), 13)

        # Extract recommended book ISBNs
        recommended_books = total_data_frame.index[indices.flatten()[1:]].tolist()

        return recommended_books


def knn_find_neighbors(book_id):
    books, ratings = load_data()
    knn = KNN()
    combine_book_rating = knn.preprocess(books, ratings)
    neighbors = knn.find_nearest_neighbors(book_id, combine_book_rating)
    return neighbors
