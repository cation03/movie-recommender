import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_embedding_model()
embedding_dim = model.get_sentence_embedding_dimension()

def compute_embeddings(movies, model):
    embeddings = []
    for movie in movies:
        emb = model.encode(movie["summary"], convert_to_numpy=True)
        norm_emb = emb / np.linalg.norm(emb)
        embeddings.append(norm_emb)
    return np.vstack(embeddings).astype("float32")

def create_faiss_index(embeddings, embedding_dim):
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(embeddings)
    return index

def compute_similarity(query_summary, index, model):
    query_emb = model.encode(query_summary, convert_to_numpy=True)
    norm = np.linalg.norm(query_emb) or 1
    query_emb = (query_emb / norm).astype("float32").reshape(1, -1)
    k = 2  # Top 2 similar movies
    scores, indices = index.search(query_emb, k)
    return indices[0], scores[0]
