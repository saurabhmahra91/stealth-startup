from pathlib import Path
import csv
import uuid
import json
from .store import model, EmbeddingChunk
from .config import EMBEDDING_FILE


CHUNK_CHAR_LIMIT = 50000


def chunk_text(text: str, limit: int) -> list[str]:
    return [text[i : i + limit] for i in range(0, len(text), limit)]


def embed_and_save(text: str, metadata: dict, output_file: Path = EMBEDDING_FILE):
    chunks = chunk_text(text, CHUNK_CHAR_LIMIT)
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        chunk_obj = EmbeddingChunk(
            id=str(uuid.uuid4()), text=chunk, embedding=embedding, metadata={**metadata, "chunk_index": i}
        )
        with open(output_file, "a") as f:
            f.write(chunk_obj.json() + "\n")


def ingest(csv_path: Path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for i, row in enumerate(rows):
        json_text = json.dumps(row, ensure_ascii=False)
        metadata = {"source": str(csv_path), "row_index": i, "columns": list(row.keys())}
        embed_and_save(json_text, metadata)


if __name__ == "__main__":
    ingest(csv_path=Path("pulse/neuron/verified_reviews.csv"))
