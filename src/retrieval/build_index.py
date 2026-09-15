import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


INPUT_FILE = "data/processed/amazon_pairs_en.jsonl"
INDEX_FILE = "data/processed/amazon_support.index"
METADATA_FILE = "data/processed/amazon_support_metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 64


def main():
    print("Loading historical AmazonHelp conversations...")

    records = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    print(f"Loaded records: {len(records):,}")

    # We only need the customer message for semantic retrieval.
    customer_texts = [
        record["customer_text"]
        for record in records
    ]

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")

    embeddings = model.encode(
        customer_texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    print(f"Embedding shape: {embeddings.shape}")

    # Inner product on normalized vectors = cosine similarity.
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"FAISS index size: {index.ntotal:,}")

    Path(METADATA_FILE).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss.write_index(index, INDEX_FILE)

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

    print(f"Saved index: {INDEX_FILE}")
    print(f"Saved metadata: {METADATA_FILE}")


if __name__ == "__main__":
    main()
    