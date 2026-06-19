from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGTrainer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def similarity_search(self, query, documents):
        corpus = [query] + documents
        vectors = self.vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(vectors[0:1], vectors[1:])
        return similarity[0]
