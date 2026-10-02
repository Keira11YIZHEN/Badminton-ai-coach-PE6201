"""Retrieval layer for the badminton knowledge base.

Primary mode uses all-MiniLM-L6-v2 sentence embeddings. If that model is
unavailable, a TF-IDF cosine fallback keeps the repository runnable and clearly
reports that the retrieval method changed.
"""
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NOTES_PATH = ROOT / 'DATA' / 'badminton_notes.json'


def load_notes(path=NOTES_PATH):
    return json.loads(Path(path).read_text(encoding='utf-8'))


class Retriever:
    def __init__(self, notes=None):
        self.notes = notes or load_notes()
        self.using = None
        texts = [n['text'] for n in self.notes]
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.matrix = self.model.encode(texts, normalize_embeddings=True)
            self.using = 'MiniLM sentence embeddings'
        except Exception:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
            self.matrix = self.vectorizer.fit_transform(texts)
            self.using = 'TF-IDF fallback'

    def _scores(self, query):
        if self.using.startswith('MiniLM'):
            q = self.model.encode([query], normalize_embeddings=True)[0]
            return np.asarray(self.matrix @ q)
        from sklearn.metrics.pairwise import cosine_similarity
        q = self.vectorizer.transform([query])
        return cosine_similarity(q, self.matrix)[0]

    def retrieve(self, query, category=None, top_k=3):
        scores = self._scores(query)
        candidates = []
        for i, note in enumerate(self.notes):
            if category is None or note['category'] == category:
                candidates.append((float(scores[i]), note))
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [{'score': score, **note} for score, note in candidates[:top_k]]
