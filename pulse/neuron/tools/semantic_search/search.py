import heapq
from pathlib import Path
import numpy as np
from .store import EmbeddingChunk
from .config import EMBEDDING_FILE


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_embeddings(file_path: Path = EMBEDDING_FILE) -> list[EmbeddingChunk]:
    chunks = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            chunks.append(EmbeddingChunk.model_validate_json(line))
    return chunks


def search(query: str, k: int, file_path: Path = EMBEDDING_FILE) -> list[str]:
    chunks = load_embeddings(file_path)

    if not chunks or k <= 0:
        return []

    if k >= len(chunks):
        return [chunk.text for chunk in chunks]

    from .store import model
    query_embedding = model.encode(query, convert_to_numpy=True)

    scored_chunks = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, np.array(chunk.embedding))
        scored_chunks.append((score, chunk.text))

    top_k = heapq.nlargest(k, scored_chunks, key=lambda x: x[0])

    return [text for _, text in top_k]


if __name__ == "__main__":
    print(search(query="Acne", k=50))
