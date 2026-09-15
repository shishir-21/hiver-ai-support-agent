import json

import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = "data/processed/amazon_support.index"
METADATA_FILE = "data/processed/amazon_support_metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3


def load_metadata():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def search(query, model, index, metadata):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )

    query_embedding = query_embedding.astype("float32")

    scores, indices = index.search(query_embedding, TOP_K)

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    for rank, (score, index_id) in enumerate(
        zip(scores[0], indices[0]),
        start=1,
    ):
        record = metadata[index_id]

        print(f"\nResult {rank}")
        print(f"Similarity: {score:.4f}")
        print(f"Customer: {record['customer_text']}")
        print(f"AmazonHelp: {record['support_text']}")


def main():
    print("Loading FAISS index...")
    index = faiss.read_index(INDEX_FILE)

    print("Loading metadata...")
    metadata = load_metadata()

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    queries = [
        "My package has not arrived yet and the delivery date has passed.",
        "I was charged for something I did not buy.",
        "I cannot log into my Amazon account.",
        "My Fire TV is not working properly.",
    ]

    for query in queries:
        search(query, model, index, metadata)


if __name__ == "__main__":
    main()
    