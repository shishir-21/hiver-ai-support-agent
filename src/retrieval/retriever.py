import json

import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = "data/processed/amazon_support.index"
METADATA_FILE = "data/processed/amazon_support_metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"


class HistoricalRetriever:

    def __init__(self):
        self.index = faiss.read_index(INDEX_FILE)

        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query, top_k=3):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )

        query_embedding = query_embedding.astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index_id in zip(scores[0], indices[0]):

            record = self.metadata[index_id]

            results.append(
                {
                    "similarity": float(score),
                    "customer_text": record["customer_text"],
                    "support_text": record["support_text"],
                    "customer_tweet_id": record["customer_tweet_id"],
                    "support_tweet_id": record["support_tweet_id"],
                }
            )

        return results
    