import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


INPUT_FILE = Path("data/processed/amazon_pairs_en.jsonl")
OUTPUT_FILE = Path("data/processed/tfidf_terms.csv")


def load_customer_messages():
    messages = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            messages.append(record["customer_text"])

    return messages


def main():
    messages = load_customer_messages()

    print(f"Loaded customer messages: {len(messages):,}")

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=20,
        max_features=60000,
        sublinear_tf=True,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z']+\b",
    )

    matrix = vectorizer.fit_transform(messages)
    terms = vectorizer.get_feature_names_out()

    mean_scores = matrix.mean(axis=0).A1

    results = pd.DataFrame(
        {
            "term": terms,
            "mean_tfidf": mean_scores,
        }
    )

    results["ngram_size"] = results["term"].str.split().str.len()

    results = results.sort_values(
        "mean_tfidf",
        ascending=False,
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print("\nTop 50 unigrams:")
    print(
        results[results["ngram_size"] == 1]
        .head(50)[["term", "mean_tfidf"]]
        .to_string(index=False)
    )

    print("\nTop 50 bigrams:")
    print(
        results[results["ngram_size"] == 2]
        .head(50)[["term", "mean_tfidf"]]
        .to_string(index=False)
    )

    print("\nTop 50 trigrams:")
    print(
        results[results["ngram_size"] == 3]
        .head(50)[["term", "mean_tfidf"]]
        .to_string(index=False)
    )

    print(f"\nSaved full results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    