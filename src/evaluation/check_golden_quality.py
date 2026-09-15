import pandas as pd


INPUT_FILE = "data/golden/amazon_golden_200.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 70)
    print("GOLDEN SET QUALITY CHECK")
    print("=" * 70)

    print(f"\nTotal rows: {len(df)}")

    # ---------------------------------------------------------
    # 1. Missing values
    # ---------------------------------------------------------

    print("\nMissing values:")
    print(df[
        [
            "customer_tweet_id",
            "support_tweet_id",
            "customer_text",
            "support_text",
        ]
    ].isna().sum())

    # ---------------------------------------------------------
    # 2. Duplicate customer messages
    # ---------------------------------------------------------

    duplicate_count = df["customer_text"].duplicated().sum()

    print(f"\nDuplicate customer messages: {duplicate_count}")

    # ---------------------------------------------------------
    # 3. Very short messages
    # ---------------------------------------------------------

    df["word_count"] = (
        df["customer_text"]
        .fillna("")
        .str.split()
        .str.len()
    )

    short_messages = df[df["word_count"] < 5]

    print(f"\nVery short messages (<5 words): {len(short_messages)}")

    for _, row in short_messages.iterrows():
        print("-" * 70)
        print(row["customer_text"])

    # ---------------------------------------------------------
    # 4. URL-heavy messages
    # ---------------------------------------------------------

    url_messages = df[
        df["customer_text"]
        .fillna("")
        .str.count("https://") >= 2
    ]

    print(f"\nURL-heavy messages: {len(url_messages)}")

    # ---------------------------------------------------------
    # 5. Context-dependent messages
    # ---------------------------------------------------------

    context_phrases = [
        "i haven't",
        "i havent",
        "i have",
        "as mentioned",
        "as i said",
        "like i said",
        "already told",
        "previous tweet",
        "above",
        "this issue",
        "this problem",
        "that issue",
        "that problem",
        "still waiting",
        "again",
    ]

    context_mask = df["customer_text"].fillna("").str.lower().apply(
        lambda text: any(
            phrase in text
            for phrase in context_phrases
        )
    )

    context_rows = df[context_mask]

    print(
        f"\nPotentially context-dependent messages: "
        f"{len(context_rows)}"
    )

    for _, row in context_rows.iterrows():
        print("-" * 70)
        print(row["customer_text"])

    # ---------------------------------------------------------
    # 6. Show random examples
    # ---------------------------------------------------------

    print("\nRandom sample of 20 messages:")

    sample = df.sample(
        n=min(20, len(df)),
        random_state=42,
    )

    for _, row in sample.iterrows():
        print("-" * 70)
        print(row["customer_text"])

    print("\nQuality check complete.")


if __name__ == "__main__":
    main()
    