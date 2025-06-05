import uuid
from pathlib import Path

from pydantic import BaseModel

from .config import EMBEDDING_FILE


class EmbeddingChunk(BaseModel):
    id: str
    text: str
    embedding: list[float]
    metadata: dict | None = {}


def embed_text(text: str, metadata: dict | None = None) -> EmbeddingChunk:
    from .model import model

    embedding = model.encode(text).tolist()
    return EmbeddingChunk(id=str(uuid.uuid4()), text=text, embedding=embedding, metadata=metadata or {})


def save_embedding(chunk: EmbeddingChunk, file_path: Path = EMBEDDING_FILE):
    with open(file_path, "a") as f:
        f.write(chunk.model_dump_json() + "\n")


def load_embeddings(file_path: Path = EMBEDDING_FILE) -> list[EmbeddingChunk]:
    chunks = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            chunks.append(EmbeddingChunk.model_validate_json(line))
    return chunks
