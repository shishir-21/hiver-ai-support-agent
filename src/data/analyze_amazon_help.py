from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/twcs.csv")
BRAND = "AmazonHelp"


def main():
    print("=" * 70)
    print("HIVER AI SUPPORT AGENT - AMAZONHELP ANALYSIS")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}")
        return

    print("\nReading dataset...")

    df = pd.read_csv(
        DATA_PATH,
        usecols=[
            "tweet_id",
            "author_id",
            "inbound",
            "created_at",
            "text",
            "response_tweet_id",
            "in_response_to_tweet_id",
        ],
    )

    print(f"Total tweets in dataset: {len(df):,}")

    # AmazonHelp support messages
    support = df[
        (df["author_id"] == BRAND) &
        (df["inbound"] == False)
    ].copy()

    print(f"AmazonHelp support tweets: {len(support):,}")

    # Customer messages
    customer = df[df["inbound"] == True].copy()

    print(f"Customer tweets: {len(customer):,}")

    # Create tweet_id -> tweet lookup
    tweet_lookup = df.set_index("tweet_id")

    customer_reply_pairs = []

    for _, support_tweet in support.iterrows():
        parent_id = support_tweet["in_response_to_tweet_id"]

        if pd.isna(parent_id):
            continue

        parent_id = int(parent_id)

        if parent_id not in tweet_lookup.index:
            continue

        parent = tweet_lookup.loc[parent_id]

        # We only want:
        # Customer message -> AmazonHelp response
        if bool(parent["inbound"]) and parent["author_id"] != BRAND:
            customer_reply_pairs.append(
                {
                    "customer_tweet_id": parent_id,
                    "support_tweet_id": int(support_tweet["tweet_id"]),
                    "customer_text": parent["text"],
                    "support_text": support_tweet["text"],
                    "customer_created_at": parent["created_at"],
                    "support_created_at": support_tweet["created_at"],
                }
            )

    pairs = pd.DataFrame(customer_reply_pairs)

    print(
        "\nDirect customer -> AmazonHelp pairs:",
        f"{len(pairs):,}",
    )

    if len(pairs) == 0:
        print("No pairs found.")
        return

    # Remove duplicate relationships
    pairs = pairs.drop_duplicates(
        subset=["customer_tweet_id", "support_tweet_id"]
    )

    print(
        "Unique customer -> AmazonHelp pairs:",
        f"{len(pairs):,}",
    )

    print("\nSample conversations:")
    print("-" * 70)

    for _, row in pairs.head(10).iterrows():
        print(f"\nCustomer [{row['customer_tweet_id']}]:")
        print(row["customer_text"])

        print(f"\nAmazonHelp [{row['support_tweet_id']}]:")
        print(row["support_text"])

        print("-" * 70)

    print("\nAmazonHelp analysis complete.")


if __name__ == "__main__":
    main()
    