import pandas as pd
from langdetect import detect, LangDetectException
import json
import random
from pathlib import Path



INPUT_FILE = Path("data/processed/amazon_pairs_en.jsonl")
OUTPUT_FILE = Path("data/golden/amazon_golden_200.csv")

RANDOM_SEED = 42
TARGET_SIZE = 200


def load_messages():
    records = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            records.append(
                {
                    "customer_tweet_id": record["customer_tweet_id"],
                    "support_tweet_id": record["support_tweet_id"],
                    "customer_text": record["customer_text"],
                    "support_text": record.get("support_text", ""),
                }
            )

    return pd.DataFrame(records)

def detect_language(text):
    try:
        return detect(str(text))
    except LangDetectException:
        return "unknown"


def keep_english_pairs(df):
    df = df.copy()

    print("\nValidating customer/support language...")

    df["customer_language"] = df["customer_text"].apply(
        detect_language
    )

    df["support_language"] = df["support_text"].apply(
        detect_language
    )

    english = df[
        (df["customer_language"] == "en")
        & (df["support_language"] == "en")
    ].copy()

    print(
        f"English customer/support pairs: "
        f"{len(english):,}"
    )

    print(
        f"Removed non-English pairs: "
        f"{len(df) - len(english):,}"
    )

    return english.drop(
        columns=[
            "customer_language",
            "support_language",
        ]
    )


def clean_for_sampling(df):
    df = df.copy()

    # Remove extremely short messages.
    df = df[df["customer_text"].str.split().str.len() >= 5]

    # Remove exact duplicate customer messages.
    df = df.drop_duplicates(subset=["customer_text"])

    # Shuffle deterministically.
    df = df.sample(frac=1, random_state=RANDOM_SEED)

    return df.reset_index(drop=True)


def sample_examples(df):
    """
    Create a diverse pool for manual annotation.

    We intentionally do not assign intent labels here.
    """

    # Take a large random pool first.
    random_pool = df.head(3000).copy()

    # Add keyword-based diversity only for SAMPLING.
    # These are NOT intent labels.
    patterns = [
        "where is",
        "not received",
        "delivered",
        "refund",
        "return",
        "prime",
        "account",
        "login",
        "password",
        "payment",
        "charged",
        "amazon pay",
        "wrong item",
        "damaged",
        "thank you",
        "cancel",
    ]

    diverse_rows = []

    for pattern in patterns:
        matches = df[
            df["customer_text"]
            .str.lower()
            .str.contains(pattern, regex=False, na=False)
        ]

        if not matches.empty:
            diverse_rows.append(
                matches.head(10)
            )

    if diverse_rows:
        diverse_pool = pd.concat(diverse_rows, ignore_index=True)
    else:
        diverse_pool = pd.DataFrame(columns=df.columns)

    combined = pd.concat(
        [random_pool, diverse_pool],
        ignore_index=True,
    )

    combined = combined.drop_duplicates(
        subset=["customer_text"]
    )

    # Shuffle again.
    combined = combined.sample(
        frac=1,
        random_state=RANDOM_SEED,
    )

    # Take final 200.
    return combined.head(TARGET_SIZE).copy()


def main():
    print("Loading cleaned AmazonHelp messages...")

    df = load_messages()

    print(f"Loaded messages: {len(df):,}")

    df = clean_for_sampling(df)

    print(f"Available after sampling cleanup: {len(df):,}")
    
    df = keep_english_pairs(df)

    golden = sample_examples(df)

    # Add empty human annotation columns.
    golden["intent"] = ""
    golden["escalation"] = ""
    golden["escalation_reason"] = ""
    golden["annotator"] = ""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    golden.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print(f"\nGolden examples created: {len(golden)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    