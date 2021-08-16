import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from itertools import combinations
from typing import List, Dict
import numpy as np
# import re
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from fasttext import FastText

nltk.download('all')
stopwords = set(stopwords.words('english'))


class SingleLangSummarizer:

    def __init__(self, ft: FastText, remove_stopwords: bool = False, lemmatize: bool = False):
        self.ft = ft
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize

    def _text_to_sentences(self, text: str) -> List[str]:
        return sent_tokenize(text.replace('\n', ' ').strip())

    def _sentence_to_vec(self, sentence: str) -> np.ndarray:
        vec = np.zeros((self.ft.get_dimension(),), dtype=np.float32)
        # res = re.sub(r'[^\w\s]', '', sentence)
        words = word_tokenize(sentence)
        for word in words:
            #             if self.remove_stopwords and word not in stopwords:
            #                 vec += self.word2vec.get_word_vector(word)
            vec += self.ft.get_word_vector(word)
        return vec / len(words)

    def _get_similarity_matrix(self, sentences: List[np.ndarray]) -> np.ndarray:
        matrix = np.zeros((len(sentences), len(sentences)), dtype=np.float32)
        for i, j in combinations(range(len(sentences)), 2):
            similarity = cosine_similarity(sentences[i].reshape(1, -1), sentences[j].reshape(1, -1))
            matrix[i][j] = matrix[j][i] = similarity
        return matrix

    def summarize(self, text: str, k: int) -> str:
        sentences = self._text_to_sentences(text)
        #         print('debug: sentences:')
        #         print(*sentences, sep='\n')
        vecs = [self._sentence_to_vec(s) for s in sentences]
        matrix = self._get_similarity_matrix(vecs)
        nx_graph = nx.from_numpy_array(matrix)
        scores = nx.pagerank(nx_graph)
        sorted_scores = sorted(list(scores.items()), key=lambda x: x[1], reverse=True)[:k]
        result_idxs = [e[0] for e in sorted(sorted_scores, key=lambda x: x[0])]
        result = ' '.join(sentences[i] for i in result_idxs)
        return result


if __name__ == '__main__':
    pass
